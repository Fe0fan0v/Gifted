from flask import Flask, render_template, redirect, request
from forms import RegisterForm, LoginForm, AddChildren
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import db_session
from models import User
from datetime import datetime

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'super_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("database.db")
db_sess = db_session.create_session()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('base.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/account', methods=['GET'])
@login_required
def my_account():
    return render_template('personal_account.html')


@app.route('/add_children', methods=['GET', 'POST'])
@login_required
def add_children():
    form = AddChildren()
    if form.validate_on_submit():
        fields = request['f']
        db_sess = db_session.create_session()
        contest = AddChildren(
            teacher=current_user.surname,
            level=form.level.data,
            nomination=form.nomination.data,
            distant=True if form.distant.data == 'Да' else False,
            union=form.union.data,
            collective=True if form.distant.data == 'Да' else False,
            place=form.place.data,
            date=datetime.strptime(form.date.data, "%d.%m.%Y"),
            # participants=[[part, pos] for part, pos in form.fio1.data, form.position1.data]
        )
    return render_template('children.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.surname == form.surname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/account")
        if not user:
            return render_template('login.html', title='Авторизация', message="Вы не зарегистрированы",
                                   form=form, color='yellow')
        return render_template('login.html', title='Авторизация', message="Неправильный логин или пароль",
                               color='red', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают.")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.surname == form.surname.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже существует")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            patronymic=form.patronymic.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/add_children')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run()
