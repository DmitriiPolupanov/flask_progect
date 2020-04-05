from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.update(SECRET_KEY = 'secret_xxx', SQLALCHEMY_DATABASE_URI  = 'sqlite:///test.db')
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        return app

class Posts(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    text = db.Column(db.String,
                     nullable=False,
                     unique=False)

class User(UserMixin, db.Model):

    __tablename__ = 'flasklogin-users'

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String,
                     nullable=False,
                     unique=False)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    created_on = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(bytes(password, encoding='utf-8'), method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

class SignupForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired()])
    email = StringField('Email',
                validators=[Length(min=6),
                            Email(message='Enter a valid email.'),
                            DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired()])
    email = StringField('Email',
                validators=[Length(min=6),
                            Email(message='Enter a valid email.'),
                            DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Login')
    
class UploadForm(FlaskForm):
    
    code_file = FileField(validators=[FileRequired()])
    submit = SubmitField('Login')
    
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('page.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def main():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect('/home')
    return redirect('/signup')
 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if request.method == 'POST':
        if signup_form.validate_on_submit():
            name = signup_form.data['name']
            email = signup_form.data['email']
            password = signup_form.data['password']
            existing_user = User.query.filter_by(email=email).first()  
            if existing_user is None:
                user = User(name=name,
                            email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                login_user(user)  
                return redirect('/home')
            return abort(418)
    return render_template('signup.html',
                           title='Create an Account.',
                           form=SignupForm(),
                           template='signup-page',
                           body="Sign up for a user account.")

@app.route('/login', methods=['GET', 'POST'])
def login():


    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            name = login_form.data['name']
            email = login_form.data['email']
            password = login_form.data['password']
            user = User.query.filter_by(email=email).first()  
            if user:
                if user.check_password(password):
                    login_user(user)  
                    return redirect('/home')
            return abort(418)
    return render_template('login.html',
                           title='Create an Account.',
                           form=LoginForm(),
                           template='signup-page',
                           body="Sign up for a user account.")

if __name__ == "__main__":


    app.run(host='0.0.0.0', debug=True)