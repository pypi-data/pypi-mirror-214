# **pgqmini**

![version](https://img.shields.io/badge/version-0.0.6-blue)
![license](https://img.shields.io/badge/license-MIT-green)

pgqmini is a lightweight, easy-to-use Python library for managing PostgreSQL message queues. It provides a simple interface for adding and retrieving messages from a PostgreSQL-based queue, as well as handling timeouts and managing message processing.

## **Table of Contents**

1. **[Installation](#installation)**
2. **[Usage](#usage)**
3. **[Contributing](#contributing)**
4. **[License](#license)**
5. **[Contact](#contact)**

## **Installation**

To install pgqmini, you can use pip:

```
pip install pgqmini
```

You also need to have a PostgreSQL server up and running. The library uses the psycopg2 package to connect to the PostgreSQL server.

## **Usage**

Here is a basic example of how to use pgqmini:

### **Publisher**
```python
from pgqmini import PGQ

pgq = PGQ(
    qname="message_queue",
    dbname="pgq",
    host="127.0.0.1",
    user="username",
    password="password",
    port=5432,
)

pgq.connect()

pgq.pub('{"key1": "value1", "key2": "value2"}')

pgq.disconnect()
```

### **Subscriber**
```python
from pgqmini import PGQ

pgq = PGQ(
    qname="message_queue",
    dbname="pgq",
    host="127.0.0.1",
    user="username",
    password="password",
    port=5432,
)

pgq.connect()

def process_message(payload: str):
    print(payload)

while True:
    pgq.sub(process_message)
```

In this code, we first create a **`PGQ`** object with the necessary database connection parameters. We then connect to the database and enter a loop where we process messages from the queue.

For a more detailed usage guide, please check out the [Usage Guide](https://github.com/over-engineers/pgqmini/wiki/PGQ-(PostgreSQL-Queue)-Class) in our wiki.


## **License**

pgqmini is released under the MIT License. See the `LICENSE` file for more details.

## **Contact**

If you have any questions, issues, or suggestions, please open an issue in this repository, or contact the maintainer at **jangsc0000@gmail.com**.
