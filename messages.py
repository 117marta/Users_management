import argparse
from models import User, Message
from confidential import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from psycopg2 import connect, OperationalError
from password import check_password


# Deklaracja argumentów (parametrów)
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password (min. 5 characters)')
parser.add_argument('-l', '--list', help='list of all messages', action='store_true')  # czy parametr jest ustawiony
parser.add_argument('-t', '--to', help='to')
parser.add_argument('-s', '--send', help='send message', type=str)  # żeby wiadomość była ze spacjami (pisać w "...")

# Metoda z parsera, która sparsuje wymagane argumenty (argumenty dostępne jako atrybut obiektu args)
args = parser.parse_args()


# Obsługa poszczególnych scenariuszy (każdy z nich to osobna funkcja)
def send_message(cur, sender_name, recipent_name, text):
    if len(text) > 255:
        print('Message is too long!')
    to = User.load_user_by_username(cur, recipent_name)
    if to:
        message = Message(from_id=sender_name, to_id=to.id, text=text)
        message.save_to_db(cur)
        print('Message sent!')
    else:
        print('Recipent does not exists!')


def print_all_user_messages(cur, user_id):
    user_messages = Message.load_all_messages(cursor=cur, user_id=user_id.id)
    for message in user_messages:
        from_ = User.load_user_by_id(cursor=cur, user_id=message.from_id)
        print(f'from: {from_.username}', f'data: {message.created}', message.text, 100 * '*', sep='\n')


# Główna część programu
if __name__ == '__main__':
    try:
        cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password:
            user = User.load_user_by_username(cursor=cursor, username=args.username)
            if check_password(pass_to_check=args.password, pass_hashed=user.hashed_password):
                if args.list:
                    print_all_user_messages(cur=cursor, user_id=user)
                elif args.to and args.send:
                    send_message(cur=cursor, sender_name=user.id, recipent_name=args.to, text=args.send)
                else:
                    parser.print_help()
            else:
                print('Incorrect password or user does not exists!')
        else:
            print('Username and password are required!')
            parser.print_help()

        # if args.username and args.password:
        #     user = User.load_user_by_username(cursor, args.username)
        #     if check_password(args.password, user.hashed_password):
        #         if args.list:
        #             print_all_user_messages(cursor, user)
        #         elif args.to and args.send:
        #             send_message(cursor, user.id, args.to, args.send)
        #         else:
        #             parser.print_help()
        #     else:
        #         print("Incorrect password or User does not exists!")
        # else:
        #     print("username and password are required")
        #     parser.print_help()

    except OperationalError as e:
        print('Connection error!', e)
    finally:
        cursor.close()
        cnx.close()


# python messages.py -u new_user -p new_password -l
# python messages.py -u new_user -p new_password -t kolejny_user -s "Wysyłam wiadomość do kolejny_user."