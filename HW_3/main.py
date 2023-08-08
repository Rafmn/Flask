'''
Создать форму для регистрации пользователей на сайте. 
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" 
и кнопку "Зарегистрироваться". При отправке формы данные должны 
сохраняться в базе данных, а пароль должен быть зашифрован.
'''

from flask import Flask, render_template, request
from model_registration import db, User
from flask_wtf.csrf import CSRFProtect
from form import RegisterForm


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:82marat19@localhost/HW_3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hw_3.db'
db.init_app(app)

app.secret_key = b'5f34214cacbd30c2ae4ssdry6784b520f17912aefge340d5d8c16ae98128e3f549546221265e4'
# получение csrf - объекта для работы с формами
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return 'Hi!'

@app.cli.command("init-db")
def init_db():
    '''Создание базы'''
    db.create_all()
    print('OK')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname =form.lastname.data
        email = form.email.data
        password = form.password.data

        # получить user из БД по email
        # можно через filter-by (только AND ???? )
        existing_user = User.query.filter((User.email == email)).first()

        # если user существует
        if existing_user:
            error_msg = 'Email already exists.'
            form.name.errors.append(error_msg)
            return render_template('register.html', form=form)

        user = User(firstname=firstname, lastname=lastname, email=email, password=password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return 'Registered success!'
    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
