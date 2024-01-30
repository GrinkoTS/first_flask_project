from flask import Flask
from flask_login import LoginManager
from config import my_key

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = my_key

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'


from app import routes