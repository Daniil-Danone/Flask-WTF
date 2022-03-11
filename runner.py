import os
import yadisk
import requests
from datetime import datetime
from static.data.crew import Crew
from static.data.jobs import Jobs
from static.data.users import User
from static.data import db_session, jobs_api
from flask_login import LoginManager, login_user, \
    login_required, logout_user, current_user
from static.python.sources import images
from static.python.weather import get_weather
from static.python.professions import professions
from static.python.loginform import RegistrationForm, \
    LoginForm, CrewLoginFormConfirm, CreateJob
from flask import Flask, render_template, request, \
    redirect, abort, make_response, jsonify


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


imgFolder = os.path.join('static')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = imgFolder


yandex_disk_token = os.environ.get('yandex_disk_API')
disk = yadisk.YaDisk(token=yandex_disk_token)


image = None


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def load_profile():
    try:
        global image
        if current_user.image_link:
            os.remove(f'static/images/avatars/avatar{current_user.id}.png')
            request = requests.get(current_user.image_link)
            with open(f'static/images/avatars/avatar{current_user.id}.png', 'wb') as f:
                f.write(request.content)
                print(f.name)
            image = f'/images/avatars/avatar{current_user.id}.png'
            return redirect('/homepage')
        return redirect('/homepage')
    except:
        return redirect('/homepage')


@app.route('/homepage', methods=['POST', 'GET'])
def default():
    weather = get_weather()
    date = datetime.now().strftime('%d %b %Y %H:%M:%S')
    return render_template('html/index.html',
                           image=image,
                           weather=weather,
                           date=date,
                           weather_image=images['weathering with you'],
                           title='Миссия колонизация Марса!',
                           elon_musk_loves_anime=images['Elon Musk cat girl'],
                           menu_bar_title='Миссия колонизация Марса!',
                           professions=professions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global image
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.image_link:
                request = requests.get(user.image_link)
                with open(f'static/images/avatars/avatar{user.id}.png', 'wb') as f:
                    f.write(request.content)
                    print(f.name)
                image = f'/images/avatars/avatar{user.id}.png'

            return redirect("/homepage")
        return render_template('html/login.html',
                               image=image,
                               incorrect_password='Неправильный логин или пароль',
                               menu_bar_title='Миссия колонизация Марса!',
                               form=form)
    return render_template('html/login.html',
                           title='Авторизация',
                           form=form,
                           image=image,
                           menu_bar_title='Миссия колонизация Марса!')


@app.route('/logout')
@login_required
def logout():
    if current_user.image_link:
        os.remove(f'static/images/avatars/avatar{current_user.id}.png')
    logout_user()
    return redirect("/")


@app.route('/login_for_crew', methods=['GET', 'POST'])
def login_for_crew():
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
                                       image=image,
                                       menu_bar_title='Миссия колонизация Марса!',
                                       incorrect_password_cap='Пароль введён неверно!')
        else:
            return render_template('html/login_for_crew.html',
                                   title='Авторизация для членов экипажа',
                                   form=form,
                                   image=image,
                                   menu_bar_title='Миссия колонизация Марса!',
                                   incorrect_login_cap='ID неверен!')
    return render_template('html/login_for_crew.html',
                           image=image,
                           title='Авторизация для членов экипажа',
                           menu_bar_title='Миссия колонизация Марса!',
                           form=form)


@app.route('/register', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    user = User()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("html/registration_form.html",
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
            user.about = request.form['text']
            user.set_password(request.form['password'])
            user.created_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
            try:
                img = form.avatar.data
                filename = f'{user.email}.png'
                img.save(f'{filename}')
                disk.upload(filename, f"/Site-avatars/{filename}")
                disk.publish(f"/Site-avatars/{filename}")
                user.image_link = disk.get_download_link(f"/Site-avatars/{filename}")
                os.remove(filename)
            except:
                pass
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            return redirect(f'/profile/{user.email}')

    return render_template("html/registration_form.html",
                           form=form,
                           title='Регистрация',
                           menu_bar_title='Миссия колонизация Марса!')


@app.route('/create_job', methods=['POST', 'GET'])
@login_required
def create_job():
    form = CreateJob()
    job = Jobs()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.id == form.team_leader_id.data).first() or \
                db_sess.query(Crew).filter(Crew.uniq_crew_id == form.team_leader_id.data).first():
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
                return redirect('/job_list')
            else:
                return render_template("html/create_job.html",
                                       form=form,
                                       image=image,
                                       card_title='Создание работы',
                                       title='Создание работы',
                                       menu_bar_title='Миссия колонизация Марса!',
                                       message='Что-то пошло не так!')
    return render_template("html/create_job.html",
                           form=form,
                           image=image,
                           card_title='Создание работы',
                           title='Создание работы',
                           menu_bar_title='Миссия колонизация Марса!')


@app.route('/edit_job/<int:id_num>', methods=['POST', 'GET'])
def edit_job(id_num):
    form = CreateJob()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id_num,
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

    if form.validate_on_submit():
        print('OK')
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id_num,
                                         Jobs.creator == current_user.id
                                         ).first()
        if db_sess.query(User).filter(User.id == form.team_leader_id.data).first() or \
                db_sess.query(Crew).filter(Crew.uniq_crew_id == form.team_leader_id.data).first():
            collabs = True
            for i in form.collaborators.data.split(', '):
                if not db_sess.query(User).filter(User.id == i).first():
                    collabs = False
                    break
            if collabs is True:
                job.job_title = form.job_title.data
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
                db_sess.commit()
                return redirect('/job_list')
            else:
                return render_template('html/create_job.html',
                                       form=form,
                                       image=image,
                                       card_title='Создание работы',
                                       title='Создание работы',
                                       menu_bar_title='Миссия колонизация Марса!',
                                       message='Что-то пошло не так!')
    return render_template('html/create_job.html',
                           form=form,
                           image=image,
                           card_title='Изменение работы',
                           title='Создание работы',
                           menu_bar_title='Миссия колонизация Марса!')


@app.route('/job_delete/<int:id_num>', methods=['GET', 'POST'])
@login_required
def news_delete(id_num):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id_num,
                                     Jobs.creator == current_user.id
                                     ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/job_list')


@app.route('/job_list', methods=['POST', 'GET'])
def job_list():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('html/job_list.html',
                           jobs=jobs,
                           image=image,
                           title='Список работ',
                           menu_bar_title='Миссия колонизация Марса!', )


@app.route('/profile/<email>', methods=['POST', 'GET'])
def answer(email):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()

    return render_template('html/auto_answer.html',
                           title='Профиль',
                           image=image,
                           params=user,
                           menu_bar_title='Миссия колонизация Марса!', )


@app.route('/training/<prof>', methods=['POST', 'GET'])
def professions_training(prof):
    if request.method == 'GET':
        return render_template('html/training_professions.html',
                               title=prof,
                               prof=prof,
                               image=image,
                               menu_bar_title='Миссия колонизация Марса!',
                               bar_back_href='/list_prof/ol',
                               bar_back_title='←Назад',
                               label_img=f'Мне сложно было найти схемы, так что вот - держите это {prof.lower()}!',
                               prof_about=professions[prof][1],
                               img_link=professions[prof][0],
                               alt=f"Ну тут должен быть {prof}")


@app.route('/list_prof/<list_type>', methods=['POST', 'GET'])
def list_professions(list_type):
    if list_type == 'ol':
        return render_template("html/list_prof.html",
                               title='Список профессий',
                               type_list='ol',
                               image=image,
                               menu_bar_title='Миссия колонизация Марса!',
                               professions=professions)
    elif list_type == 'ul':
        return render_template("html/list_prof.html",
                               title='Список профессий',
                               type_list='ul',
                               image=image,
                               menu_bar_title='Миссия колонизация Марса!',
                               professions=professions)


@app.route('/distribution/', methods=['POST', 'GET'])
def distribution():
    db_sess = db_session.create_session()
    data_members = [[user.surname, user.name, user.sex, user.email, user.studying, user.professions, user.about,
                     user.created_date] for user in db_sess.query(User).all()]
    db_sess = db_session.create_session()
    data_crew = [[user.surname, user.name, user.post, user.email, user.studying, user.professions, user.about,
                  user.created_date] for user in db_sess.query(Crew).all()]

    return render_template("html/distribution.html",
                           title='Список профессий',
                           image=image,
                           menu_bar_title='Миссия колонизация Марса!',
                           rooms=[data_crew, data_members],
                           shift=len(data_crew))


if __name__ == '__main__':
    db_session.global_init("static/databases/my_site.db")
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=8080, host='127.0.0.1', debug=True)
