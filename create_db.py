from confidential import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable


# Add queries to variables
CREATE_DB = f"CREATE DATABASE {DB_NAME};"

CREATE_USERS_TABLE = """CREATE TABLE users(
    id serial PRIMARY KEY,
    username varchar(255) UNIQUE,
    hashed_password varchar(80))"""

CREATE_MESSAGES_TABLE = """CREATE TABLE messages(
    id SERIAL,
    from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    to_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    text varchar(255),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""


#  CREATE DATABASE
try:
    cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)  # łączenie się z serwerem
    cnx.autocommit = True  # transakcje wyłączone
    print('Connected successfully!')
    try:
        cur = cnx.cursor()  # wysyłanie zapytania przez cursor
        cur.execute(CREATE_DB)  # zapytanie do BD
        print('Database created!')
    except DuplicateDatabase as err:
        print("Database exists!", err)
except OperationalError as err:
    print('Connection error!', err)
finally:
    cur.close()
    cnx.close()


#  CREATE TABLES
def execute_sql(sql, db):
    try:
        connexion = connect(user=DB_USER, password=DB_PASSWORD, database=db, host=DB_HOST)  # connection to created DB
        connexion.autocommit = True
        cursor = connexion.cursor()
        try:
            cursor.execute(sql)
            print('Query committed!')
        except DuplicateTable as error:
            print('Duplicate table!', error)
    except OperationalError as error:
        print('Connection error!', error)
    finally:
        cursor.close()
        connexion.close()


create_users_table = execute_sql(CREATE_USERS_TABLE, DB_NAME)
create_messages_table = execute_sql(CREATE_MESSAGES_TABLE, DB_NAME)
