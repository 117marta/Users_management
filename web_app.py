from psycopg2 import connect, OperationalError
from flask import Flask, render_template, request, session, redirect, url_for, render_template_string

from confidential import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from password import check_password


app = Flask(__name__)  # aktualny plik będzie serwerem Flask


LOGIN_FORM = """
<form method="POST">
    <p>Username: <input type=text name=username></p>
    <label for="password">Password:</label>
    <input type="password" name="password"><br>
    <input type="submit" value="Zaloguj">
</form>
"""


@app.route('/')
def index():
    if 'username' in session:
        print("Currents user's ID is: %s" % session.get('id'))
        return render_template_string(
            """
            <p>Zalogowano jako <strong>{{ (session['username']) }}</strong>
            <a href={{ url_for('logout') }}><button>Wyloguj</button></a></p>
            <p><a href={{ url_for('get_messages') }}>Wiadomości</a>
            <a href={{ url_for('get_users') }}>Użytkownicy</a></p>
            """
        )
    return render_template_string(
        """
        <p>Nie zalogowano!
        <a href={{ url_for('login') }}><button>Zaloguj</button></a></p>
        """
    )


@app.route('/logout')
def logout():
    session.pop('username', None)  # remove the username from the session if it's there
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        current_user = request.form['username']
        current_password = request.form['password']
        SQL = f"SELECT * FROM users WHERE username='{current_user}'"
        rows = execute_sql(sql=SQL, db=DB_NAME)
        database_user = rows[0][1] if rows else False
        database_password = rows[0][2] if rows else False
        if current_user == database_user and check_password(current_password, database_password):
            session['username'] = request.form['username']
            session["logged"] = True
            return redirect(url_for('index'))
        else:
            return 'Wprowadź poprawny login i/lub hasło!'
    return LOGIN_FORM  # GET method


def execute_sql(sql, db):
    try:
        cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=db)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql)
        print('Query commited!')
        return cursor.fetchall()
    except OperationalError as err:
        print('Connection error!', err)
    finally:
        cursor.close()
        cnx.close()


@app.route("/messages/")
def get_messages():
    SQL = "SELECT * FROM messages"
    rows = execute_sql(sql=SQL, db=DB_NAME)
    return render_template(template_name_or_list="messages.html", rows=rows)


@app.route("/users/")
def get_users():
    # SQL = "SELECT id, username FROM users"
    SQL = "SELECT * FROM users"
    rows = execute_sql(sql=SQL, db=DB_NAME)
    return render_template(template_name_or_list="users.html", rows=rows)


app.secret_key = '5fd02cfcae9788b77476bb72dbba47170b83a3b66362b82676d632541a0a6768'


if __name__ == "__main__":
    app.run(debug=True)
