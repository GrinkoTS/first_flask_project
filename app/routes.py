from flask import render_template
from app import app

@app.route('/index')
@app.route('/')
def index():
    my_value = 'МИР'
    return render_template('index.html', my_value = my_value)
    #return '<h1> Привет, мир! </h1> <p> В этом параграфе я выведу <a href="https://yandex.ru/"> ссылку на яндекс </a> </p>'
