from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional 

class LoginForm(FlaskForm):
    name = StringField('Имя',
                       validators=[DataRequired()])
    email = StringField('Электронный адресс',
                validators=[Length(min=6),
                            Email(message='Введите правильный электронный адресс.'),
                            DataRequired()])
    password = PasswordField('Пароль',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Подтвердите пароль',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Вход')
    
class SignupForm(FlaskForm):
    name = StringField('Имя',
                       validators=[DataRequired()])
    email = StringField('Электронный адрес',
                validators=[Length(min=6),
                            Email(message='Enter a valid email.'),
                            DataRequired()])
    password = PasswordField('Пароль',
                             validators=[DataRequired(),
                                         Length(min=6, message='Пароль недостаточно надежный.')])
    confirm = PasswordField('Подтвердите пароль',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Пароли должны совпадать.')])
    submit = SubmitField('Регистрация')
   
   
class UploadForm(FlaskForm):
    lat = StringField('lat', validators=[DataRequired()])
    lng = StringField('lng', validators=[DataRequired()])
    name = StringField('Название', validators=[DataRequired()])
    desc = StringField('Описание', validators=[DataRequired()])
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Регистрация')