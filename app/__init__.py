from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Конфигурация
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-12345'
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(os.path.dirname(basedir), 'medai.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Создание таблиц
    with app.app_context():
        from app.models import User
        db.create_all()

    # Регистрация blueprints
    from app.routes import auth_bp, admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
