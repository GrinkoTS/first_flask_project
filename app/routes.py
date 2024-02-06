from flask import render_template, request, flash, redirect, url_for, session, abort
from app import app
import datetime
from werkzeug.security import check_password_hash
import app.models as m
from flask_login import login_user, login_required, current_user, logout_user

@app.route('/index')
@app.route('/')
def index():
    now = datetime.datetime.now()

    day_period = {'morning': 'Доброе утро!',
                  'day': 'Добрый день!',
                  'evening': 'Добрый вечер!',
                  'night': 'Доброй ночи!'}

    products = ['Шапки', 'Шарфы', 'Чепчики', 'Кардиганы', 'Жилетки', 'Пледы']

    return render_template('index.html', date=now, day_period=day_period, products=products)




@app.route('/Шапки')
def hats():
    return render_template('hats.html', title="Magic hats")

@app.route('/Шарфы')
def scarves():
    return render_template('scarves.html', title="Magic scarves")

@app.route('/Чепчики')
def caps():
    return render_template('cap.html', title="Magic caps")

@app.route('/Кардиганы')
def cardigans():
    return render_template('cardigans.html', title="Magic cardigans")

@app.route('/Жилетки')
def waistcoats():
    return render_template('waistcoats.html', title="Magic waistcoats")

@app.route('/Пледы')
def wraps():
    return render_template('wraps.html', title="Magic wraps")

@app.route('/Регистрация', methods=('POST', 'GET'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    elif request.method == 'POST':
        user = m.check_user()
        if user:
            flash('Адрес электронной почты уже существует')
            return redirect(url_for('register'))
        elif len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            answer = m.addUser()
            if answer == True:
                flash('Вы успешно зарегестрированы')
            else:
                flash('Ошибка добавления в БД')
        else:
            flash('Неверно заполнены поля')
    return render_template('register.html', title='Регистрация')

@app.route('/Войти', methods=('POST', 'GET'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        user = m.check_user()
        if user:
            if not user.email or not check_password_hash(user.psw, request.form['psw']):
                flash('Неверное имя пользователя и/или пароль')
                return redirect(url_for('login'))
            else:
                rm = True if request.form.get('remainme') else False
                login_user(user, remember=rm)
                return redirect(request.args.get('next') or url_for('profile'))
        else:
            flash('Данный пользователь не зарегистрирован')
            return redirect(url_for('register'))
    return render_template('login.html', title="Авторизация")

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта",  'success')
    return redirect(url_for('login'))

@app.route('/tg_bot')
@login_required
def tg_bot():
    if current_user.is_authenticated:
        return redirect("https://t.me/Memobot_for_you_bot")


