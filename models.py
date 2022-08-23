from password import hash_password


class User:

    def __init__(self, username="", password="", salt=None):
        # nie powinien być dostępny do edycji z zewnątrz - poza klasą (_id)
        # nowo utworzony obiekt nie będzie od razu synchronizowany (-1). Dane z DB != -1
        self._id = -1  # tylko do odczytu
        self.username = username
        self._hashed_password = hash_password(password, salt)  # tylko do odczytu

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
        # Modyfikacja obiektu (user w bazie)
        else:
            sql = """UPDATE users SET username=%s, hashed_password=%s
                    WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    # Wczytanie jednego rzędu z BD i zamienienie go w obiekt
    @staticmethod  # funkcja jest statyczna (wywołujemy ją na klasie, a nie na obiekcie). Nie potrzeba instacji obiektu (usera) żeby wczytać innych użytkowników
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

    # Wyszukiwanie usera po nazwie
    @staticmethod
    def load_user_by_username(cursor, username):
        sql = """SELECT id, username, hashed_password FROM users
                WHERE username=%s"""
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            user_id, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = user_id
            loaded_user._hashed_password = hashed_password
            return loaded_user

    # Wczytanie wiele obiektów
    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            # (7, 'kolejny_user4', 'sol_do_hashowanib624e0de9d7f94c5a4b550c7009826f47b7e17b3fca21fc08efaf290f802bd39')
            user_id, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = user_id
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    # Usunięcie obiektu z BD
    def delete_user(self, cursor):
        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1  # obiekt został usunięty (więc jego id to -1)
        return True


class Message:

    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._created = None

    @property
    def id(self):
        return self._id

    @property
    def created(self):
        return self._created

    # Zapisanie wiadomości do BD
    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text)
                            VALUES (%s, %s, %s) RETURNING id, created"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self._created = cursor.fetchone()  # fetchone() zwraca krotkę
            return True
        else:
            sql = """UPDATE messages SET from_id=%s, to_id=%s, text=%s
                    WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            return True

    # Załadowanie wiadomości
    @staticmethod
    def load_all_messages(cursor, sender, recipient):
        if recipient:
            sql = "SELECT id, from_id, to_id, text, created FROM messages WHERE to_id=%s"
            cursor.execute(sql, (recipient,))
        elif sender:
            sql = "SELECT id, from_id, to_id, text, created FROM messages WHERE from_id=%s"
            cursor.execute(sql, (sender,))
        else:
            sql = "SELECT id, from_id, to_id, text, created FROM messages"
            cursor.execute(sql)
        messages = []
        for row in cursor.fetchall():
            # (5, 4, 9, 'Wiadomość testowa!', datetime.datetime(2022, 7, 10, 19, 48, 27, 934419))
            user_id, from_id, to_id, text, created = row
            loaded_message = Message(from_id, to_id, text)
            loaded_message._id = user_id
            loaded_message._created = created
            messages.append(loaded_message)
        return messages
