from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)

# Маршруты аутентификации
@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Создание нового пользователя
            user = User(
                full_name=form.full_name.data,
                email=form.email.data,
                iin=form.iin.data if form.auth_type.data == 'iin' else None,
                phone=form.phone.data if form.auth_type.data == 'phone' else None
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            flash('Успешно зарегистрированы! Теперь вы можете войти.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при регистрации: {str(e)}', 'danger')

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        login_input = form.login.data
        password = form.password.data

        # Поиск пользователя по email, ИИН или телефону
        user = User.query.filter(
            (User.email == login_input) |
            (User.iin == login_input) |
            (User.phone == login_input)
        ).first()

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', 'success')
    return redirect(url_for('auth.login'))


# Маршруты администратора
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('admin.users'))


@admin_bp.route('/users')
@login_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=10)
    return render_template('users.html', users=users)


@admin_bp.route('/user/<int:user_id>')
@login_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)
