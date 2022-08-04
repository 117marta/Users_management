from psycopg2 import connect, OperationalError, errors
from flask import Flask, render_template, request, session, redirect, url_for, render_template_string, flash
import datetime
import time

from confidential import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from password import check_password, hash_password


app = Flask(__name__)  # aktualny plik będzie serwerem Flask
app.secret_key = '5fd02cfcae9788b77476bb72dbba47170b83a3b66362b82676d632541a0a6768'  # session to be available


USER_FORM = """
{% extends "base.html" %}
{% block title %}Form{% endblock %}
{% block content %}
<h1>{{ 'Login' if 'login' in request.url else 'Create an account' }}</h1>
<form method="POST">
    <p>Username: <input type=text name=username maxlength="30" placeholder="Enter the username"></p>
    <p>Password: <input type="password" name="password" maxlength="30" placeholder="Enter the password"></p>
    <button type="submit" name="submit" style="background-color:black; color:gold; border-color:red; height:30px; width:100px">Send</button>
</form>
{% endblock %}
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


def execute_sql_no_returning(sql, db):
    try:
        cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=db)
        cnx.autocommit = True
        cur = cnx.cursor()
        print('Connected successfully!')
        cur.execute(sql)
    except OperationalError as err:
        print('Connection error!', err)
    finally:
        cur.close()
        cnx.close()


@app.route('/')
def index():
    context = {
        'now': datetime.datetime.utcnow(),
        'strftime': time.strftime,
    }
    if 'username' in session:
        print("Currents user's ID is: %s" % session.get('id'))
        context.update({'username_from_session': session['username']})
    return render_template(template_name_or_list='index.html', **context)


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
            flash('You are logged in!')
            return redirect(url_for('index'))
        else:
            flash('Enter the correct login and/or password!')
            return redirect(url_for('login'))
    return render_template_string(source=USER_FORM)


@app.route('/logout')
def logout():
    session.clear()
    flash('You were successfully logged out!')
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


@app.route("/users/create", endpoint='create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            if len(password) < 5:
                flash(message='Password must be at least 5 characters!')
                return redirect(location=url_for(endpoint='create_user'))
            else:
                password = hash_password(password)
                SQL = f"INSERT INTO users(username, hashed_password) VALUES ('{username}', '{password}');"
                try:
                    execute_sql_no_returning(sql=SQL, db=DB_NAME)
                except errors.UniqueViolation:
                    flash(message='User already exists!')
                    return redirect(location=url_for(endpoint='create_user'))
                flash(message='User created!')
                return redirect(location=url_for(endpoint='index'))
        else:
            flash(message='Invalid data!')
            return redirect(location=url_for(endpoint='create_user'))
    else:
        return render_template_string(source=USER_FORM)


if __name__ == "__main__":
    app.run(debug=True)
