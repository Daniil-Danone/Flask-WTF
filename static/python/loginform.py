from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField, RadioField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                          name='surname',
                          id='surname',
                          render_kw={"placeholder": "Введите фамилию..."},)

    name = StringField('Имя', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                       name='name',
                       id='name',
                       render_kw={"placeholder": "Введите имя..."})

    email = EmailField('Почта', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                            Email(message='Неверный адрес почты')],
                       name='email',
                       id='email',
                       render_kw={"placeholder": "Введите почту..."})

    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                   Length(min=4, max=32,
                                                          message='Длина пароля должна составлять от 4 до 32 символов!')],
                             id='password',
                             name='password',
                             render_kw={"placeholder": "Придумайте пароль..."})

    sex = RadioField('Пол', validators=[DataRequired('Пол не выбран!')],
                     choices=[('Мужчина', 'Мужской'), ('Женщина', 'Женский')],
                     id='sex',
                     name='sex',)

    studying = SelectField('Образование', choices=[('', '-- Выберите вариант --'),
                                                   ('Низшее', 'Низшее'),
                                                   ('Среднее', 'Среднее'),
                                                   ('Высшее', 'Высшее'),
                                                   ('Никакое', 'Никакое'),
                                                   ('Какое образование? Я гуль!', 'Какое образование? Я гуль!')],
                           validators=[DataRequired(message='Это поле должно быть заполнено!')],
                           id='studying',
                           name='studying')

    engineer = BooleanField('Инженер (человек, умеющий настраивать Wi-Fi)',
                            id='engineer',
                            name='engineer',
                            render_kw={"value": "Инженер"})

    pilot = BooleanField('Пилот (человек, умеющий отличать газ от тормоза)',
                         id='pilot',
                         name='pilot',
                         render_kw={"value": "Пилот"})

    builder = BooleanField('Строитель (человек, знающий как надо построить ферму '
                           'и чтобы её не снесло как в "Марсианине)',
                           id='builder',
                           name='builder',
                           render_kw={"value": "Строитель"})

    coolman = BooleanField('Серьёзный дядька, делающий вид, что чем-то занимается',
                           id='coolman',
                           name='coolman',
                           render_kw={"value": "Серьёзный дядька"})

    fatman = BooleanField('Весёлый дядька, который подчищает запасы провизии',
                          id='fatman',
                          name='fatman',
                          render_kw={"value": "Весёлый дядька"})

    instagirl = BooleanField('Инстасамка (ну тут и так всё понятно)',
                             id='instagirl',
                             name='instagirl',
                             render_kw={"value": "Инстасамка"})

    chemist = BooleanField('Химик (желательно грамотный и без приколов)',
                           id='chemist',
                           name='chemist',
                           render_kw={"value": "Химик"})

    doctor = BooleanField('Доктор (человек, умеющий клеить пластыри на скафандр '
                          'и обрабатывать вмятины зелёнкой)',
                          id='doctor',
                          name='doctor',
                          render_kw={"value": "Врач"})

    text = TextAreaField('Расскажите, почему Вы решили лететь на Марс? Одумайтесь, пока не поздно...',
                         id='text',
                         name='text',
                         render_kw={"placeholder": "Введите текст..."})

    accept = BooleanField('Соглашение', validators=[DataRequired(message='Вы должны согласиться!')],
                          id='accept',
                          name='accept')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                            Email(message='Неверный адрес почты')],
                       name='email',
                       id='email',
                       render_kw={"placeholder": "Введите логин (почту)..."})

    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                   Length(min=4, max=32,
                                                          message='Длина пароля должна составлять от 4 до 32 символов!')],
                             id='password',
                             name='password',
                             render_kw={"placeholder": "Введите пароль..."})

    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    submit_crew = SubmitField('Продолжить')


class CreateJob(FlaskForm):
    job_title = StringField('Название работы',
                            validators=[DataRequired(message='Это поле должно быть заполнено!')],
                            name='job_title',
                            id='job_title',
                            render_kw={"placeholder": "Введите название работы..."})

    job_describe = TextAreaField('Описание работы',
                                 id='job_describe',
                                 name='job_describe',
                                 render_kw={"placeholder": "Опишите работу, что нужно делать сотрудникам..."})

    team_leader_id = StringField('ID тим-лида',
                                 validators=[DataRequired(message='Это поле должно быть заполнено!')],
                                 name='team_leader_id',
                                 id='team_leader_id',
                                 render_kw={"placeholder": "Введите ID тим-лида..."})
    work_size = StringField('Объём работы (в часах)',
                            validators=[DataRequired(message='Это поле должно быть заполнено!')],
                            name='work_size',
                            id='work_size',
                            render_kw={"placeholder": "Введите количество часов..."})
    collaborators = StringField('Сотрудники',
                                validators=[DataRequired(message='Это поле должно быть заполнено!')],
                                name='collaborators',
                                id='collaborators',
                                render_kw={"placeholder": "Введите ID сотрудников через запятую..."})
    start_date = StringField('Начало работ',
                             validators=[DataRequired(message='Это поле должно быть заполнено!')],
                             name='start_date',
                             id='start_date',
                             render_kw={"placeholder": "Введите дату начала работ..."})
    end_date = StringField('Окончание работ',
                           validators=[DataRequired(message='Это поле должно быть заполнено!')],
                           name='end_date',
                           id='end_date',
                           render_kw={"placeholder": "Введите планируемую дату окончания работ..."})
    is_finished = BooleanField('Работа окончена?')


class CrewLoginFormConfirm(FlaskForm):
    id_captain = EmailField('ID капитана', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                            name='id_captain',
                            id='id_captain',
                            render_kw={"placeholder": "Введите ID капитана..."})

    password_captain = PasswordField('Пароль капитана', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                           Length(min=4, max=32,
                                                                  message='Длина пароля должна составлять от 4 до 32 символов!')],
                                     id='password_captain',
                                     name='password_captain',
                                     render_kw={"placeholder": "Введите пароль капитана..."})

    id_astr = EmailField('ID астронавта', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                            name='id_astr',
                            id='id_astr',
                            render_kw={"placeholder": "Введите ID астронавта..."})

    password_astr = PasswordField('Пароль астронавта', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                             Length(min=4, max=32,
                                                                    message='Длина пароля должна составлять от 4 до 32 символов!')],
                                       id='password_astr',
                                       name='password_astr',
                                       render_kw={"placeholder": "Введите пароль астронавта..."})

    submit_crew_confirm = SubmitField('Подтвердить')

