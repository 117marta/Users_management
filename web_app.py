from confidential import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from psycopg2 import connect, OperationalError
from flask import Flask, render_template


app = Flask(__name__)  # aktualny plik będzie serwerem Flask


def execute_sql(sql, db):
    try:
        cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=db)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql)
        print('Query commited!')
        return cursor
        # return list(cursor)  # wyniki zapytania w formie listy
        # return cursor.fetchall()
    except OperationalError as err:
        print('Connection error!', err)


@app.route("/messages/")
def get_messages():
    SQL = "SELECT * FROM messages"
    rows = execute_sql(sql=SQL, db=DB_NAME)
    # return render_template(template_name_or_list="messages.html", rows=rows)
    sql_result = '{msg_id} | {from_id} | {to_id} | {created} | {text} </br>'
    for (msg_id, from_id, to_id, created, text) in rows:
        sql_result += f'{msg_id} | {from_id} | {to_id} | {created} | {text} </br>'
    return sql_result


if __name__ == "__main__":
    app.run(debug=True)
