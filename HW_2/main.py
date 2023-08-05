'''
Создать страницу, на которой будет форма для ввода имени и электронной почты, 
при отправке которой будет создан cookie-файл с данными пользователя, а также 
будет произведено перенаправление на страницу приветствия, где будет отображаться 
имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет 
удалён cookie-файл с данными пользователя и произведено перенаправление на страницу 
ввода имени и электронной почты.
'''

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4ry6784b520f17912aefge340d5d8c16ae98128e3f549546221265e4'

@app.route('/')
def index():
    if 'name' in session:
        name = {session["name"]}
        return render_template('hello.html', name=name)
    else:
        return redirect(url_for('submit_get'))

@app.route('/submit', methods=['GET', 'POST'])
def submit_get():
    if request.method == 'POST':
        session['name'] = request.form.get('name') or 'NoName'
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.pop('name', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
