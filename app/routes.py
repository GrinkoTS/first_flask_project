from flask import render_template
from app import app
import datetime

@app.route('/index')
@app.route('/')
def index():
    now = datetime.datetime.now()

    day_period = {'morning': 'Доброе утро!',
                  'day': 'Добрый день!',
                  'evening': 'Добрый вечер!',
                  'night': 'Доброй ночи!'}

    products = ['Шапки', 'Шарфы', 'Чепчики', 'Кардиганы', 'Жилетки', 'Носочки', 'Пледы']

    return render_template('index.html', date=now, day_period=day_period, products=products)


@app.route('/Шапки')
def hats():
    return render_template('hats.html')

@app.route('/Шарфы')
def scarves():
    return render_template('scarves.html')