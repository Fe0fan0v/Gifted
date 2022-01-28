from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать')


class LoginForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddChildren(FlaskForm):
    teacher = StringField('Преподаватель')
    level = SelectField('Уровень мероприятия', choices=['Международный', 'Федеральный', 'Региональный', 'Муниципальный',
                                                        'Институциональный'])
    nomination = StringField('Номинация')
    distant = SelectField('Дистанционный', choices=['Да', 'Нет'])
    union = StringField('Объединение')
    collective = SelectField('Коллектив', choices=['Да', 'Нет'])
    place = StringField('Место проведение')
    date = StringField('Дата проведения (Пример: 20.12.2022)')
    send = SubmitField('Отправить')
    fio1 = StringField('ФИО')
    position1 = StringField('Место')
    fio2 = StringField('ФИО')
    position2 = StringField('Место')
    fio3 = StringField('ФИО')
    position3 = StringField('Место')
    fio4 = StringField('ФИО')
    position4 = StringField('Место')
    fio5 = StringField('ФИО')
    position5 = StringField('Место')
    fio6 = StringField('ФИО')
    position6 = StringField('Место')
    fio7 = StringField('ФИО')
    position7 = StringField('Место')
    fio8 = StringField('ФИО')
    position8 = StringField('Место')
    fio9 = StringField('ФИО')
    position9 = StringField('Место')
    fio10 = StringField('ФИО')
    position10 = StringField('Место')
    fio11 = StringField('ФИО')
    position11 = StringField('Место')
    fio12 = StringField('ФИО')
    position12 = StringField('Место')
    fio13 = StringField('ФИО')
    position13 = StringField('Место')
    fio14 = StringField('ФИО')
    position14 = StringField('Место')
    fio15 = StringField('ФИО')
    position15 = StringField('Место')
    participants = dict()
