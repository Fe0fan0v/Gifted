from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, SelectField, FormField, Form, FieldList
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


class Participant(Form):
    fio = StringField('ФИО')
    position = StringField('Место')


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
    participants = FieldList(FormField(Participant), min_entries=1, max_entries=15)
