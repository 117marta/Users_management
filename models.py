from password import hash_password
from confidential import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from psycopg2 import connect


# USER CLASS

class User:

    def __init__(self, username="", password="", salt=""):
        # nie powinien być dostępny do edycji z zewnątrz - poza klasą (_id)
        # nowo utworzony obiekt nie będzie od razu synchronizowany (-1). Dane z DB != -1
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property  # udostępniamy na zewnątrz klasy
    def id(self):  # id trzyma klucz główny lub wartość -1
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):  # potrzeba przekazać sól (setter nie przekazuje parametru)
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter  # wygeneruje sól automatycznie
    def hashed_password(self, password):
        self.set_password(password)

    # Synchronizuje nasz obiekt z BD
    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES (%s, %s) RETURNING id;"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # przypisujemy klucz główny jako id (jeśli udało się zapisać obiekt do BD)
            # self._id = cursor.fetchone()['id']
            return True
        # Modyfikacja obiektu
        else:
            sql = """UPDATE users SET username=%s, hasehed_password=%s
                    WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    # Wczytanie jednego rzędu z BD i zamienienie go w obiekt
    @staticmethod  # funkcja jest statyczna (wywołujemy ją na klasie, a nie na obiekcie)
    def load_user_by_id(cursor, user_id):
        sql = """SELECT id, username, hashed_password FROM users
                WHERE id=%s"""
        cursor.execute(sql, (user_id,))
        data = cursor.fetchone()
        if data:
            user_id, username, hashed_password = data  # rozpakowanie danych do odpowiednich zmiennych
            loaded_user = User(username)  # jesteśmy w środku klasy (dostęp do własności niedostępnych na zewnątrz)
            loaded_user._id = user_id
            loaded_user._hashed_password = hashed_password  # hasło z BD w formie zahaszowanej (nie używamy settera)
            return loaded_user
        else:
            return None

    # Wczytanie wiele obiektów
    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            user_id, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = user_id
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users


########################################################################################################################
# Do testowania...

cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
cnx.autocommit = True
cur = cnx.cursor()

# u1 = User('user_1', 'silne_hasło', 'gYrcy8xsm49lIq1r')
# u1.save_to_db(cur)

u2 = User()
get_user = u2.load_user_by_id(cur, 1)
print(get_user.username)

u3 = User
get_users = u3.load_all_users(cur)
print(get_users)

u4 = User('user_zmodyfikowany', 'silne_hasło2', 'gYrcy8xsm49lIq1r')
update_user = u4.save_to_db(cur)
print('uuuu', update_user)
