from confidential import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from psycopg2 import connect, OperationalError
from flask import Flask, render_template, request, session, escape, redirect, url_for


app = Flask(__name__)  # aktualny plik będzie serwerem Flask


LOGIN_FORM = """
<form method="POST">
    <p>Username: <input type=text name=username></p>
    <label for="password">Password:</label>
    <input type="password" name="password"><br>
    <input type="submit" value="Zaloguj">
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    # POST method
    if request.method == 'POST':
        session['username'] = request.form['username']
        # session['password'] = request.form['password']
        # session['email'] = request.form.get('email')
        # session['id'] = request.form.get('id')
        return redirect(url_for('index'))
    # GET method
    return LOGIN_FORM


@app.route('/')
def index():
    if 'username' in session:
        print("Currents user's ID is: %s" % session.get('id'))
        return 'Logged in as <strong>%s</strong>' % escape(session['username'])  # escaping for you if you are not using the template engine
    return 'You are not logged in'


@app.route('/logout')
def logout():
    session.pop('username', None)  # remove the username from the session if it's there
    return redirect(url_for('index'))


app.secret_key = '5fd02cfcae9788b77476bb72dbba47170b83a3b66362b82676d632541a0a6768'


if __name__ == "__main__":
    app.run(debug=True)
