from psycopg2 import connect, OperationalError
from flask import Flask, render_template, request, session, redirect, url_for, render_template_string

from confidential import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from password import check_password


app = Flask(__name__)  # aktualny plik będzie serwerem Flask
app.secret_key = '5fd02cfcae9788b77476bb72dbba47170b83a3b66362b82676d632541a0a6768'  # session to be available


LOGIN_FORM = """
<form method="POST">
    <p>Username: <input type=text name=username placeholder="Enter the username"></p>
    <label for="password">Password:</label>
    <input type="password" name="password" placeholder="Enter the password"><br>
    <input type="submit" value="Login">
</form>
"""


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


@app.route('/')
def index():
    if 'username' in session:
        print("Currents user's ID is: %s" % session.get('id'))
        return render_template_string(
            """
            <p>Logged as: <strong>{{ (session['username']) }}</strong>
            <a href={{ url_for('logout') }}><button>Logout</button></a></p>
            <p><a href={{ url_for('get_messages') }}>Messages</a>
            <a href={{ url_for('get_users') }}>Users</a></p>
            """
        )
    return render_template_string(
        """
        <p>You are not logged in!
        <a href={{ url_for('login') }}><button>Login</button></a></p>
        """
    )


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
            return 'Enter the correct login and/or password!'
    return LOGIN_FORM  # GET method


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route("/messages/")
def get_messages():
    if not session.get('username'):
        return redirect(location=url_for(endpoint='login'))
    SQL = "SELECT * FROM messages"
    rows = execute_sql(sql=SQL, db=DB_NAME)
    return render_template(template_name_or_list="messages.html", rows=rows)


@app.route("/users/")
def get_users():
    if not session.get('username'):
        return redirect(location=url_for(endpoint='login'))
    # SQL = "SELECT id, username FROM users"
    SQL = "SELECT * FROM users"
    rows = execute_sql(sql=SQL, db=DB_NAME)
    return render_template(template_name_or_list="users.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
