from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    iin = db.Column(db.String(12), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        """Установить хешированный пароль"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверить пароль"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.full_name}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
