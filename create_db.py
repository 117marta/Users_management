from confidential import DB_USER, PASSWORD, HOST

# Add queries to variables
CREATE_DB = "CREATE DATABASE users_management;"

CREATE_USERS_TABLE = """CREATE TABLE users(
    id serial PRIMARY KEY,
    username varchar(255) UNIQUE,
    hashed_password varchar(80))"""

CREATE_MESSAGES_TABLE = """CREATE TABLE messages(
    id SERIAL,
    from_id INTEGER REFERENCES user(id) ON DELETE CASCADE,
    to_id INTEGER REFERENCES user(id) ON DELETE CASCADE,
    text varchar(255),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
