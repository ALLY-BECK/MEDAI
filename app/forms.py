from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators
from app.models import User

class RegistrationForm(FlaskForm):
    full_name = StringField('Полное имя', validators=[
        validators.DataRequired('Поле обязательно'),
        validators.Length(min=2, max=120, message='Имя должно быть от 2 до 120 символов')
    ])

    auth_type = RadioField('Выберите способ регистрации', choices=[
        ('iin', 'По ИИН'),
        ('phone', 'По номеру телефона')
    ], validators=[validators.DataRequired()])

    iin = StringField('ИИН (12 цифр)', validators=[
        validators.Optional(),
        validators.Regexp(r'^\d{12}$', message='ИИН должен содержать 12 цифр')
    ])

    phone = StringField('Номер телефона', validators=[
        validators.Optional(),
        validators.Regexp(r'^\+?\d{10,}$', message='Введите корректный номер телефона')
    ])

    email = StringField('Email', validators=[
        validators.DataRequired('Поле обязательно'),
        validators.Email('Некорректный email'),
    ])

    password = PasswordField('Пароль', validators=[
        validators.DataRequired('Поле обязательно'),
        validators.Length(min=6, message='Пароль должен быть минимум 6 символов')
    ])

    confirm_password = PasswordField('Подтверждить пароль', validators=[
        validators.DataRequired('Поле обязательно'),
        validators.EqualTo('password', message='Пароли не совпадают')
    ])

    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise validators.ValidationError('Email уже используется')

    def validate_iin(self, field):
        if self.auth_type.data == 'iin' and field.data:
            if User.query.filter_by(iin=field.data).first():
                raise validators.ValidationError('Этот ИИН уже зарегистрирован')

    def validate_phone(self, field):
        if self.auth_type.data == 'phone' and field.data:
            if User.query.filter_by(phone=field.data).first():
                raise validators.ValidationError('Этот номер телефона уже зарегистрирован')


class LoginForm(FlaskForm):
    login = StringField('ИИН, номер телефона или Email', validators=[
        validators.DataRequired('Поле обязательно')
    ])

    password = PasswordField('Пароль', validators=[
        validators.DataRequired('Поле обязательно')
    ])

    submit = SubmitField('Войти')
