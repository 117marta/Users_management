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
        return False


########################################################################################################################
# Do testowania...

cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
cnx.autocommit = True
cur = cnx.cursor()

u1 = User('user_1', 'silne_hasło', 'gYrcy8xsm49lIq1r')
u1.save_to_db(cur)
