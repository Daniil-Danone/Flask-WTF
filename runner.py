import os
import sqlite3
from datetime import datetime
from static.data.users import User
from static.data.crew import Crew
from static.data.jobs import Jobs
from static.data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from static.other.professions import professions
from static.python.loginform import RegistrationForm, LoginForm, CrewLoginFormConfirm, CreateJob
from flask import Flask, render_template, request, redirect, abort


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


imgFolder = os.path.join('static', 'img')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
#  app.config['UPLOAD_FOLDER'] = imgFolder   -  позже пригодится


user_info = {}


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("static/databases/my_site.db")
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
    db_session.global_init("static/databases/my_site.db")
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


@app.route('/login_for_crew', methods=['GET', 'POST'])
def login_for_crew():
    db_session.global_init("static/databases/my_site.db")
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


@app.route('/register', methods=['POST', 'GET'])
def registration():
    html_file = "html/registration_form.html"
    form = RegistrationForm()
    user = User()

    db_session.global_init("static/databases/my_site.db")

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


@app.route('/create_job', methods=['POST', 'GET'])
@login_required
def create_job():
    html_file = "html/create_job.html"
    form = CreateJob()
    job = Jobs()
    db_session.global_init("static/databases/my_site.db")
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.id == form.team_leader_id.data).first() or db_sess.query(Crew).filter(Crew.uniq_crew_id == form.team_leader_id.data).first():
            collabs = True
            for i in form.collaborators.data.split(', '):
                if not db_sess.query(User).filter(User.id == i).first():
                    collabs = False
                    break
            if collabs is True:
                job.job_title = form.job_title.data
                print(form.job_describe.data)
                if len(form.job_describe.data) > 40:
                    text = ''
                    output_text = ''
                    for i in form.job_describe.data.split():
                        if len(i) + len(text) < 40:
                            text = text + i + ' '
                        else:
                            output_text = output_text + text + '\n'
                            text = i + " "
                    output_text = output_text + text
                    job.job_describe = output_text
                else:
                    job.job_describe = form.job_describe.data
                job.team_leader = form.team_leader_id.data
                job.work_size = form.work_size.data
                job.collaborators = form.collaborators.data
                job.start_date = form.start_date.data
                job.end_date = form.end_date.data
                job.is_finished = form.is_finished.data
                job.creator = current_user.id
                db_sess.merge(current_user)
                db_sess.add(job)
                db_sess.commit()
                return redirect('/')
            else:
                return render_template(html_file,
                                       form=form,
                                       card_title='Создание работы',
                                       title='Создание работы',
                                       menu_bar_title='Миссия колонизация Марса!',
                                       message='Что-то пошло не так!')
    return render_template(html_file,
                           form=form,
                           card_title='Создание работы',
                           title='Создание работы',
                           menu_bar_title='Миссия колонизация Марса!')


@app.route('/edit_job/<int:id>', methods=['POST', 'GET'])
def edit_job(id):
    form = CreateJob()
    html_file = "html/create_job.html"
    db_session.global_init("static/databases/my_site.db")
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         Jobs.creator == current_user.id
                                         ).first()
        if job:
            form.job_title.data = job.job_title
            form.job_describe.data = ' '.join(job.job_describe.split())
            form.team_leader_id.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.start_date.data = job.start_date
            form.end_date.data = job.end_date
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    return render_template(html_file,
                           form=form,
                           card_title='Изменение работы',
                           title='Создание работы',
                           menu_bar_title='Миссия колонизация Марса!')


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id,
                                     Jobs.creator == current_user.id
                                     ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/job_list', methods=['POST', 'GET'])
def job_list():
    html_file = 'html/job_list.html'
    db_session.global_init("static/databases/my_site.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template(html_file,
                           jobs=jobs,
                           title='Список работ',
                           menu_bar_title='Миссия колонизация Марса!', )


@app.route('/profile/<email>', methods=['POST', 'GET'])
def answer(email):
    db_session.global_init("static/databases/my_site.db")
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
    db_session.global_init("static/databases/my_site.db")
    db_sess = db_session.create_session()
    data_members = [[user.surname, user.name, user.sex, user.email, user.studying, user.professions, user.about,
                     user.created_date] for user in db_sess.query(User).all()]
    db_sess = db_session.create_session()
    data_crew = [[user.surname, user.name, user.post, user.email, user.studying, user.professions, user.about,
                  user.created_date] for user in db_sess.query(Crew).all()]

    return render_template(html_file,
                           title='Список профессий',
                           menu_bar_title='Миссия колонизация Марса!',
                           rooms=[data_crew, data_members],
                           shift=len(data_crew))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
