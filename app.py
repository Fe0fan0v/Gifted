from flask import Flask, render_template, redirect, request, url_for, send_file
from forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import db_session
from models import User, Contest
from datetime import datetime, date
import json

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'super_secret_key'
DOWNLOAD_FOLDER = 'downloads/'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("database.db")
db_sess = db_session.create_session()


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('base.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/download/<contest>')
def download(contest):
    # file_path = DOWNLOAD_FOLDER + ...
    # return send_file(file_path, as_attachment=True, attachment_filename='filename')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def my_account():
    if current_user.type == 'teacher':
        return render_template('personal_account.html')
    else:
        if request.method == 'POST':
            start_date = datetime.strptime(request.form.get('start-date'), "%Y-%m-%d")
            finish_date = datetime.strptime(request.form.get('finish-date'), "%Y-%m-%d")
            teachers = request.form.getlist('teachers')
            db_sess = db_session.create_session()
            contests = {}
            for teacher in teachers:
                finded = db_sess.query(Contest).filter(Contest.teacher == teacher,
                                                       Contest.date >= start_date, Contest.date <= finish_date)
                finded = [x.serialize for x in finded.all()]
                contests[teacher] = []
                contests[teacher].append(*finded)
            return redirect(url_for('results', teachers=json.dumps(contests, default=json_serial)))
        else:
            db_sess = db_session.create_session()
            teachers = [user.surname for user in db_sess.query(User).all()]
            return render_template('methodist_account.html', teachers=teachers)


@app.route('/results/<teachers>')
@login_required
def results(teachers):
    teachers = json.loads(teachers)
    return render_template('search_results.html', teachers=teachers)


@app.route('/add_children', methods=['GET', 'POST'])
@login_required
def add_children():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        data = request.form
        info = data.to_dict()
        fios = data.getlist('fio[]')
        positions = data.getlist('position[]')
        participants = {}
        for i in range(len(fios)):
            participants[fios[i]] = positions[i]
        contest = Contest(
            teacher=current_user.surname,
            level=info['level'],
            nomination=info['nomination'],
            distant=True if info['distant'] == 'Да' else False,
            union=info['union'],
            collective=True if info['distant'] == 'Да' else False,
            place=info['place'],
            date=datetime.strptime(info['date'], "%d.%m.%Y"),
            participants=participants
        )
        db_sess.add(contest)
        db_sess.commit()
    return render_template('children.html')


@app.route('/my_contests', methods=['GET'])
@login_required
def my_contests():
    db_sess = db_session.create_session()
    contests = db_sess.query(Contest).filter(Contest.teacher == current_user.surname).all()
    return render_template('contests.html', contests=contests)


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
        login_user(user)
        return redirect('/account')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run()
