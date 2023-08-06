from dataclasses import dataclass, asdict
import select
from typing import Any, Callable
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2


@dataclass(frozen=True)
class Message:
    """
    A class that represents a message in the queue.
    It is an immutable class, hence decorated with the 'frozen=True' parameter.
    """

    id: int  # Unique identifier for the message
    payload: str  # The actual content of the message, which is a JSON-formatted string


@dataclass(frozen=True)
class QueueInfo:
    """
    A class that represents the information necessary to connect to the queue.
    It is an immutable class, hence decorated with the 'frozen=True' parameter.
    """

    host: str  # The hostname of the database server
    user: str  # The username to connect to the database
    password: str  # The password to connect to the database
    port: int  # The port number on which the database server is listening
    dbname: str  # The name of the database
    qname: str  # The name of the queue


class PGQ:
    """
    The PGQ (PostgreSQL Queue) class represents a queue in a PostgreSQL database.
    It allows for the publishing and subscribing of messages to and from the queue.

    The PGQ class manages the connection to the PostgreSQL database, the creation of the database and queue (if they do not already exist),
    and the insertion and retrieval of messages from the queue.

    Each message in the queue has a status, which can be 'PENDING', 'PROCESSING', or 'COMPLETED'.
    When a new message is inserted into the queue, its status is set to 'PENDING'.
    When a message is retrieved from the queue for processing, its status is set to 'PROCESSING'.
    If the message is processed successfully, its status is updated to 'COMPLETED'.
    If an exception occurs during the processing of the message, its status is rolled back to 'PENDING'.

    The PGQ class also provides a method for rolling back the status of messages that have been in the 'PROCESSING' state for longer than a specified timeout.

    Attributes:
        conn: A psycopg2 connection object for the PostgreSQL database.
        curs: A cursor object for executing PostgreSQL commands.
        qinfo: An instance of the QueueInfo dataclass, which stores the information necessary to connect to the queue.
    """

    conn: Any
    curs: Any
    qinfo: QueueInfo

    def __init__(self, host, user, password, port, dbname="pgq", qname="message_queue"):
        """
        The constructor of the PGQ class. It sets up the necessary variables to establish a connection to a PostgreSQL database.
        It also sets up a logger for logging purposes.

        :param host: The hostname of the database server.
        :param user: The username to connect to the database.
        :param password: The password to connect to the database.
        :param port: The port number on which the database server is listening.
        :param dbname: The name of the database. Defaults to 'pgq'.
        :param qname: The name of the queue. Defaults to 'message_queue'.
        """
        self.logger = logging.getLogger(__name__)

        self.qinfo = QueueInfo(host, user, password, port, dbname, qname)

    def _create_db(self):
        """
        A private method that creates a new database if it does not already exist.
        It does this by first connecting to the default 'postgres' database.
        """
        dbinfo = asdict(self.qinfo)
        dbinfo.update(dbname="postgres", qname=None)

        conn = psycopg2.connect(**dbinfo)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        curs = conn.cursor()

        try:
            curs.execute(
                f"""
                    -- Create a database
                    CREATE DATABASE {self.qinfo.dbname};
                """
            )
        except psycopg2.errors.DuplicateDatabase as e:
            pass
        finally:
            curs.close()
            conn.close()

    def _create_queue(self):
        """
        A private method that creates a new table (queue) in the database if it does not already exist.
        It also sets up the necessary triggers and trigger functions for the queue.
        """
        try:
            self.curs.execute(
                f"""
                    -- Create a table
                    CREATE TYPE message_status AS ENUM ('PENDING', 'PROCESSING', 'COMPLETED');

                    CREATE TABLE {self.qinfo.qname} (
                        id SERIAL PRIMARY KEY,
                        payload JSON NOT NULL,
                        status message_status NOT NULL DEFAULT 'PENDING',
                        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );

                    -- Create indexes on status, updated_at columns
                    CREATE INDEX idx_{self.qinfo.qname}_status ON {self.qinfo.qname}(status);
                    CREATE INDEX idx_{self.qinfo.qname}_updated_at ON {self.qinfo.qname}(updated_at);

                    -- Create a function
                    CREATE OR REPLACE FUNCTION update_updated_at_column()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.updated_at = NOW();
                        -- Rollback
                        IF (NEW.status = 0 AND NEW.status <> OLD.status) THEN
                            PERFORM pg_notify('new_message', NEW.id::text);
                        END IF;
                        RETURN NEW;
                    END;
                    $$ language 'plpgsql';                  

                    -- Create a trigger
                    CREATE OR REPLACE TRIGGER update_{self.qinfo.qname}_updated_at
                    BEFORE UPDATE ON {self.qinfo.qname}
                    FOR EACH ROW
                    EXECUTE PROCEDURE update_updated_at_column();

                    -- Create a trigger function
                    CREATE OR REPLACE FUNCTION notify_insert_message() RETURNS TRIGGER AS $$
                    DECLARE
                    BEGIN
                        -- Trigger an event named 'new_message', passing the ID of the new row
                        PERFORM pg_notify('new_message', NEW.id::text);
                        RETURN NEW;
                    END;
                    $$ LANGUAGE plpgsql;

                    -- Define a trigger to call the trigger function whenever a new row is inserted in the table
                    CREATE OR REPLACE TRIGGER {self.qinfo.qname}_trigger
                    AFTER INSERT ON {self.qinfo.qname}
                    FOR EACH ROW EXECUTE PROCEDURE notify_insert_message();
                """
            )
        except psycopg2.errors.DuplicateTable as e:
            pass

    def connect(self):
        """
        Connects to the PostgreSQL database and creates a cursor object for executing PostgreSQL commands.
        It also calls the _create_db and _create_queue methods to ensure that the database and queue are set up.
        """
        self._create_db()

        dbinfo = asdict(self.qinfo)
        dbinfo.update(qname=None)
        self.conn = psycopg2.connect(**dbinfo)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.curs = self.conn.cursor()

        self._create_queue()

    def disconnect(self):
        """
        Closes the cursor and the connection to the PostgreSQL database.
        """
        self.curs.close()
        self.conn.close()

    def pub(self, payload):
        """
        Inserts a new message into the queue with the specified payload.

        :param payload: The actual content of the message, which is a JSON-formatted string.
        """
        self.curs.execute(
            f"""
                -- Insert a message into the queue
                INSERT INTO {self.qinfo.qname} (payload)
                VALUES ('{payload}');
            """
        )

    def sub(self, callback: Callable[[str], None]):
        """
        Subscribes to the queue and continuously processes new messages as they arrive.
        When a new message is processed, the specified callback function is called with the message's payload.

        :param callback: A function to be called when a new message is processed. This function should take a single argument, which is the payload of the message.
        """
        self.curs.execute("LISTEN new_message;")

        try:
            while True:
                msg = None
                self.curs.execute(
                    f"""
                        -- Select a message to process and update its status to 'PROCESSING'
                        UPDATE {self.qinfo.qname}
                        SET status = 'PROCESSING'
                        FROM (
                            -- Select a message from the queue
                            SELECT id FROM {self.qinfo.qname}
                            WHERE status = 'PENDING'
                            ORDER BY id
                            FOR UPDATE SKIP LOCKED
                            LIMIT 1
                        ) sub
                        WHERE {self.qinfo.qname}.id = sub.id
                        RETURNING {self.qinfo.qname}.id, payload
                    """
                )

                # Fetch the message to be processed
                row = self.curs.fetchone()

                if row is None:
                    select.select([self.conn], [], [])
                    continue
                msg = Message(id=row[0], payload=row[1])

                callback(msg.payload)
                self._complete_message(msg)
                return
        except Exception as e:
            if msg:
                self._rollback_message(msg)
            raise Exception

    def _complete_message(self, msg: Message):
        """
        A private method that updates the status of a message to 'COMPLETED' after it has been processed.

        :param msg: The message that has been processed.
        """
        self.curs.execute(
            f"""
                -- Update the status of a message to 'COMPLETED'
                UPDATE {self.qinfo.qname}
                SET status = 'COMPLETED'
                WHERE id = {msg.id}
            """
        )

    def _rollback_message(self, msg: Message):
        """
        A private method that updates the status of a message to 'PENDING' if an exception occurs during the processing of the message.

        :param msg: The message whose processing resulted in an exception.
        """
        self.curs.execute(
            f"""
                -- Update the status of a message to 'PENDING'
                UPDATE {self.qinfo.qname}
                SET status = 'PENDING'
                WHERE id = {msg.id}
            """
        )

    def rollback_timeout_messages(self, timeout: int):
        """
        Updates the status of all messages that have been in the 'PROCESSING' state for longer than the specified timeout to 'PENDING'.

        :param timeout: The number of seconds after which a message in the 'PROCESSING' state is considered to have timed out.
        """
        self.curs.execute(
            f"""
                -- Update the status of messages to 'PENDING' if they have timed out
                UPDATE {self.qinfo.qname}
                SET status = 'PENDING'
                WHERE status='PROCESSING' and updated_at + interval '{timeout} seconds' < now()
           """
        )
