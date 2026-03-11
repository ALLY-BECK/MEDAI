from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Конфигурация
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-12345')

    # Используем DATABASE_URL если задан (PostgreSQL), иначе SQLite в /tmp (для Vercel)
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Heroku/Railway передают postgres://, SQLAlchemy требует postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # /tmp — единственная writable директория на Vercel
        db_path = os.path.join('/tmp', 'medai.db')
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
