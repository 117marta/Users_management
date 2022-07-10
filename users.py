import argparse
from models import User
from confidential import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation
from password import check_password


# Deklaracja argumentów (parametrów)
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password (min. 5 characters)')
parser.add_argument('-n', '--new_pass', help='new password (min. 5 characters)')
parser.add_argument('-l', '--list', help='list of all users', action='store_true')  # czy parametr jest ustawiony
parser.add_argument('-d', '--delete', help='delete user', action='store_true')
parser.add_argument('-e', '--edit', help='edit user', action='store_true')

# Metoda z parsera, która sparsuje wymagane argumenty
args = parser.parse_args()


# Obsługa poszczególnych scenariuszy (każdy z nich to osobna funkcja)
def create_user(cur, username, password):
    if len(password) < 5:
        print('Password is too short! It must have minimum 5 characters.')
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cur)
            print('User created!')
        except UniqueViolation as err:
            print('User already exists!', err)


def delete_user(cur, username, password):
    user = User.load_user_by_username(cur, username)
    if not user:
        print('User does not exists!')
    elif check_password(password, user.hashed_password):
        user.delete_user(cur)
        print('User deleted!')
    else:
        print('Incorrect password!')


def edit_user(cur, username, password, new_password):
    user = User.load_user_by_username(cur, username)
    if not user:
        print('User does not exists!')
    elif check_password(password, user.hashed_password):
        if len(password) < 5:
            print('Password is too short! It must have minimum 5 characters.')
        else:
            user.hashed_password = new_password
            user.save_to_db(cur)
            print('Password changed!')
    else:
        print('Incorrect password!')


def list_all_users(cur):
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)
