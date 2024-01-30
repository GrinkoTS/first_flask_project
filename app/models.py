from app import app, login_manager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import request
from flask_login import UserMixin


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f'<users {self.id}>'

class Profiles(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<profiles {self.id}>'

class Products(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_tg_id = db.Column(db.Integer)
    products = db.Column(db.String(200))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

'''with app.app_context():
    db.create_all()'''

def addUser(*args, **kwargs):
    result = False
    try:
        # генерируем хэш пароля для сохранения в БД
        hash = generate_password_hash(request.form['psw'])
        # добавляем пользователя в БД
        u = Users(email=request.form['email'], psw=hash)
        with app.app_context():
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['name'], old=request.form['old'],
                           city=request.form['city'], user_id=u.id)

            db.session.add(p)
            db.session.commit()
            result = True
        return result
    except:
        with app.app_context():
            db.session.rollback()
        return result

def check_user():
    email = request.form['email']
    with app.app_context():
        user = db.session.query(Users).filter(Users.email == f'{email}').first()
    return user

@login_manager.user_loader
def load_user(user_id):
    return Profiles.query.get(int(user_id))













