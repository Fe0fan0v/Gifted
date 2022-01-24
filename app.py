from flask import Flask, render_template, redirect
from forms import RegisterForm, LoginForm, AddChildren
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import db_session
from models import User

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


@app.route('/add_children', methods=['GET', 'POST'])
def add_children():
    form = AddChildren()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        contest = AddChildren(
            teacher=current_user.surname,

        )
    return render_template('children.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.surname == form.surname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/add_children")
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
