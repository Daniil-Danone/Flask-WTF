import os
import sqlite3
from datetime import datetime
from static.data.users import User
from static.data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user
from static.other.professions import professions
from static.python.loginform import RegistrationForm, LoginForm, CrewLoginFormConfirm
from flask import Flask, render_template, request, redirect


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


imgFolder = os.path.join('static', 'img')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
#  app.config['UPLOAD_FOLDER'] = imgFolder   -  позже пригодится


user_info = {}


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("static/databases/blogs.db")
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['POST', 'GET'])
def default():
    html_file = 'html/index.html'
    return render_template(html_file,
                           title='Миссия колонизация Марса!',
                           menu_bar_title='Миссия колонизация Марса!',
                           professions=professions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db_session.global_init("static/databases/blogs.db")
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('html/login.html',
                               incorrect_password='Неправильный логин или пароль',
                               menu_bar_title='Миссия колонизация Марса!',
                               form=form)
    return render_template('html/login.html', title='Авторизация', form=form, menu_bar_title='Миссия колонизация Марса!')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


'''@app.route('/login', methods=['GET', 'POST'])
def login():
    db_session.global_init("static/databases/blogs.db")
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.email == request.form['email']).first():
            return render_template('html/login.html',
                                   title='Авторизация',
                                   form=form,
                                   incorrect_login='Аккаунта с таким логином не существует! '
                                                   'Пожалуйста, проверьте правильность его ввода.',
                                   menu_bar_title='Миссия колонизация Марса!')

        else:
            user = db_sess.query(User).filter(User.email == request.form['email']).first()
            if user.check_password(request.form['password']):
                return redirect(f'/profile/{request.form["email"]}')
            else:
                return render_template('html/login.html',
                                       title='Авторизация',
                                       form=form,
                                       menu_bar_title='Миссия колонизация Марса!',
                                       incorrect_password='Пароль введён неверно!')

    return render_template('html/login.html',
                           title='Авторизация',
                           form=form,
                           menu_bar_title='Миссия колонизация Марса!')'''


@app.route('/login_for_crew', methods=['GET', 'POST'])
def login_for_crew():
    db_session.global_init("static/databases/blogs.db")
    form = CrewLoginFormConfirm()
    if form.validate_on_submit():
        data = login_check_crew_db(request.form['id_captain'])
        if data:
            if data[5] == request.form['password_captain']:
                return redirect('/success')
            elif data[5] != request.form['password_captain']:
                return render_template('html/login_for_crew.html',
                                       title='Авторизация для членов экипажа',
                                       form=form,
                                       menu_bar_title='Миссия колонизация Марса!',
                                       incorrect_password_cap='Пароль введён неверно!')
        else:
            return render_template('html/login_for_crew.html',
                                   title='Авторизация для членов экипажа',
                                   form=form,
                                   menu_bar_title='Миссия колонизация Марса!',
                                   incorrect_login_cap='ID неверен!')
    return render_template('html/login_for_crew.html',
                           title='Авторизация для членов экипажа',
                           menu_bar_title='Миссия колонизация Марса!',
                           form=form)


@app.route('/success', methods=['GET', 'POST'])
def success():
    return 'Вход выполнен'


@app.route('/register', methods=['POST', 'GET'])
def reg():
    html_file = "html/registration_form.html"
    form = RegistrationForm()
    user = User()

    db_session.global_init("static/databases/blogs.db")

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(html_file,
                                   form=form,
                                   title='Регистрация',
                                   menu_bar_title='Миссия колонизация Марса!',
                                   email_exist='Пользователь с данной почтой уже существует!')
        else:
            user.surname = request.form['surname']
            user.name = request.form['name']
            user.email = request.form['email']
            user.hashed_password = request.form['password']
            user.studying = request.form['studying']
            profs = []
            for i in ['engineer', 'pilot', 'builder', 'coolman', 'fatman', 'instagirl', 'doctor']:
                try:
                    profs.append(request.form[i])
                except:
                    continue

            user.professions = ', '.join(profs)
            user.sex = request.form['sex']
            user.about = request.form['about']
            user.set_password(request.form['password'])
            user.created_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            return redirect(f'/profile/{user.email}')

    return render_template(html_file,
                           form=form,
                           title='Регистрация',
                           menu_bar_title='Миссия колонизация Марса!')


@app.route('/profile/<email>', methods=['POST', 'GET'])
def answer(email):
    db_session.global_init("static/databases/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    html_file = 'html/auto_answer.html'
    return render_template(html_file,
                           title='Профиль',
                           params=user,
                           menu_bar_title='Миссия колонизация Марса!', )


@app.route('/training/<prof>', methods=['POST', 'GET'])
def professions_training(prof):
    if request.method == 'GET':
        html_file = 'html/training_professions.html'
        return render_template(html_file,
                               title=prof,
                               prof=prof,
                               menu_bar_title='Миссия колонизация Марса!',
                               bar_back_href='/list_prof/ol',
                               bar_back_title='←Назад',
                               label_img=f'Мне сложно было найти схемы, так что вот - держите это {prof.lower()}!',
                               prof_about=professions[prof][1],
                               img_link=professions[prof][0],
                               alt=f"Ну тут должен быть {prof}")


@app.route('/list_prof/<list_type>', methods=['POST', 'GET'])
def list_professions(list_type):
    html_file = "html/list_prof.html"
    if list_type == 'ol':
        return render_template(html_file,
                               title='Список профессий',
                               type_list='ol',
                               menu_bar_title='Миссия колонизация Марса!',
                               professions=professions)
    elif list_type == 'ul':
        return render_template(html_file,
                               title='Список профессий',
                               type_list='ul',
                               menu_bar_title='Миссия колонизация Марса!',
                               professions=professions)


@app.route('/distribution/', methods=['POST', 'GET'])
def distribution():
    html_file = "html/distribution.html"

    data_crew = get_all_crew()
    data_members = get_all_members()

    return render_template(html_file,
                           title='Список профессий',
                           menu_bar_title='Миссия колонизация Марса!',
                           rooms=[data_crew, data_members],
                           shift=len(data_crew))


def insert_data_to_db(surname, name, email, password, sex, studying, profs, about, reg_data):
    con = sqlite3.connect('static/databases/site_users.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (id_num INTEGER PRIMARY KEY, surname TEXT, name TEXT, email TEXT, 
    password TEXT, sex TEXT, studying TEXT, profs TEXT, about TEXT, reg_data TEXT)''')

    cur.execute('''INSERT into users (surname, name, email, password, sex, studying, profs, about, reg_data) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (surname, name, email, password, sex, studying, profs, about, reg_data))

    con.commit()
    con.close()


def login_check_db(email):
    con = sqlite3.connect('static/databases/site_users.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (id_num INTEGER PRIMARY KEY, surname TEXT, name TEXT, email TEXT, 
        password TEXT, sex TEXT, studying TEXT, profs TEXT, about TEXT, reg_data TEXT)''')

    data = cur.execute(f'''SELECT * FROM users WHERE email=?''', (email,)).fetchone()

    con.commit()
    con.close()
    return data


def login_check_crew_db(id):
    con = sqlite3.connect('static/databases/site_crew.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS crew (id_num INTEGER PRIMARY KEY, id INT, surname TEXT, name TEXT, email TEXT, 
            password TEXT, sex TEXT, studying TEXT, profs TEXT, about TEXT, reg_data TEXT)''')

    data = cur.execute(f'''SELECT * FROM crew WHERE id=?''', (id,)).fetchone()

    con.commit()
    con.close()
    return data


def get_all_crew():
    con = sqlite3.connect('static/databases/site_crew.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS crew (id_num INTEGER PRIMARY KEY, id INT, surname TEXT, name TEXT, email TEXT, 
                password TEXT, sex TEXT, studying TEXT, profs TEXT, about TEXT, reg_data TEXT)''')

    data = cur.execute(f'''SELECT * FROM crew''').fetchall()

    con.commit()
    con.close()
    return data


def get_all_members():
    con = sqlite3.connect('static/databases/site_users.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (id_num INTEGER PRIMARY KEY, surname TEXT, name TEXT, email TEXT, 
            password TEXT, sex TEXT, studying TEXT, profs TEXT, about TEXT, reg_data TEXT)''')

    data = cur.execute(f'''SELECT * FROM users''').fetchall()

    con.commit()
    con.close()
    return data


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
