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


# CREATE DATABASE
def create_database():
    try:
        cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)  # łączenie się z serwerem
        cnx.autocommit = True  # transakcje wyłączone
        cur = cnx.cursor()  # utworzenie kursora (wysłanie zapytania przez cursor)
        print('Connected successfully!')
        try:
            cur.execute(CREATE_DB)  # zapytanie do BD
            print('Database created!')
        except DuplicateDatabase as err:
            print("Database exists!", err)
        except OperationalError as err:
            print('Connection error!', err)
    finally:
        cur.close()
        cnx.close()


# CREATE TABLES
def create_table(sql, db):
    try:
        connexion = connect(user=DB_USER, password=DB_PASSWORD, database=db, host=DB_HOST)  # połączenie z utworzoną BD
        connexion.autocommit = True
        cursor = connexion.cursor()
        try:
            cursor.execute(sql)
            print('Table created!')
        except DuplicateTable as error:
            print('Duplicate table!', error)
    except OperationalError as error:
        print('Connection error!', error)
    finally:
        cursor.close()
        connexion.close()


if __name__ == "__main__":  # aby uniknąć wywoływania kodu w przypadku importowania z tego pliku (zabezpieczenie)
    create_database()
    create_users_table = create_table(CREATE_USERS_TABLE, DB_NAME)
    create_messages_table = create_table(CREATE_MESSAGES_TABLE, DB_NAME)
