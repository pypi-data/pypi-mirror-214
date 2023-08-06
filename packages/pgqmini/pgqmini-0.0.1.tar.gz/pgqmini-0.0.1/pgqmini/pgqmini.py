from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from dataclasses import dataclass, asdict
from typing import Any
import select


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
    A class for managing a PostgreSQL-based message queue.
    """

    conn: Any
    curs: Any
    qinfo: QueueInfo

    def __init__(self, host, user, password, port, dbname="pgq", qname="message_queue"):
        """
        Initialize the instance with connection details.
        """
        self.qinfo = QueueInfo(host, user, password, port, dbname, qname)

    def _create_db(self):
        """
        A private method to create a database if it doesn't already exist.
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
        A private method to create a queue if it doesn't already exist.
        """
        try:
            self.curs.execute(
                f"""
                    -- Create a table
                    CREATE TABLE {self.qinfo.qname} (
                        id SERIAL PRIMARY KEY,
                        payload JSON NOT NULL,
                        status VARCHAR(10) NOT NULL DEFAULT 'PENDING',
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
                       RETURN NEW;
                    END;
                    $$ language 'plpgsql';                  

                    -- Create a trigger
                    CREATE TRIGGER update_{self.qinfo.qname}_updated_at
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
        Establishes the connection to the PostgreSQL server and creates the queue.
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
        Closes the connection to the PostgreSQL server.
        """
        self.curs.close()
        self.conn.close()

    def pub_message(self, payload):
        """
        Publishes a new message to the queue.
        """
        self.curs.execute(
            f"""
                -- Insert a message into the queue
                INSERT INTO {self.qinfo.qname} (payload)
                VALUES ('{payload}');
            """
        )

    def sub_message(self):
        """
        Subscribes to the queue and selects a pending message to process.
        """
        self.curs.execute("LISTEN new_message;")
        while True:
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
            msg = self.curs.fetchone()
            if msg is None:
                select.select([self.conn], [], [])
                continue
            return Message(id=msg[0], payload=msg[1])

    def complete_message(self, msg: Message):
        """
        Marks a message as completed. The input is a Message object.
        """
        self.curs.execute(
            f"""
                -- Update the status of a message to 'COMPLETED'
                UPDATE {self.qinfo.qname}
                SET status = 'COMPLETED'
                WHERE id = {msg.id}
            """
        )

    def complete_message_by_id(self, id: int):
        """
        Marks a message as completed by its ID.
        """
        self.curs.execute(
            f"""
                -- Update the status of a message to 'COMPLETED' by its ID
                UPDATE {self.qinfo.qname}
                SET status = 'COMPLETED'
                WHERE id = {id}
            """
        )

    def rollback_message(self, msg: Message):
        """
        Reverts the status of a message to 'PENDING'. The input is a Message object.
        """
        self.curs.execute(
            f"""
                -- Update the status of a message to 'PENDING'
                UPDATE {self.qinfo.qname}
                SET status = 'PENDING'
                WHERE id = {msg.id}
            """
        )

    def rollback_message_by_id(self, id: int):
        """
        Reverts the status of a message to 'PENDING' by its ID.
        """
        self.curs.execute(
            f"""
                -- Update the status of a message to 'PENDING' by its ID
                UPDATE {self.qinfo.qname}
                SET status = 'PENDING'
                WHERE id = {id}
            """
        )

    def rollback_timeout_messages(self, timeout: int):
        """
        Reverts the status of messages that have timed out to 'PENDING'.
        """
        self.curs.execute(
            f"""
                -- Update the status of messages to 'PENDING' if they have timed out
                UPDATE {self.qinfo.qname}
                SET status = 'PENDING'
                WHERE status='PROCESSING' and updated_at + interval '{timeout} seconds' < now()
           """
        )
