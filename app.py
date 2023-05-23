import requests
from flask import Flask, render_template, request, redirect
import psycopg2


app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="",        #paste here the password every time since i ve changed it
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            if username == '':
                return render_template('login.html', error = 'Поле логина не может быть пустым')
            password = request.form.get('password')
            if password == '':
                return render_template('login.html', error = 'Поле пароля не может быть пустым')
            cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(username),))
            records = list(cursor.fetchall())
            if records == []:
                return render_template('login.html', error = 'Пользователя не бывает')
            else:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
                records = list(cursor.fetchall())
                if records == []:
                    return render_template('login.html', error = 'Неверный пароль')
                else:
                    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if name == '' or login == '' or password == '':
            return render_template('registration.html', error_reg = 'Поля не должны оставаться пустыми')
        cursor.execute("SELECT * FROM service.users WHERE login=%s ", (str(login), ))
        records = list(cursor.fetchall())
        if records:
            return render_template('registration.html', error_reg = 'Логин занят')
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')

    return render_template('registration.html')


if __name__ == '__main__':
    app.run()



