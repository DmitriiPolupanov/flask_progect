from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, current_user, login_user
from flask import current_app as app
from .forms import LoginForm, SignupForm
from .models import db, User
from .import login_manager

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@auth_bp.route('/signup', methods=['GET', 'POST'])
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
            error=dict(head='Ошибка регистрации', body='Такой пользователь уже существует')
            return render_template('error.html', error=error)
    return render_template('signup.html',
                           title='Create an Account.',
                           form=SignupForm(),
                           template='signup-page',
                           body="Sign up for a user account.")

@auth_bp.route('/login', methods=['GET', 'POST'])
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
            error=dict(head='Ошибка авторизации', body='Такого пользователя не существует')
            return render_template('error.html', error=error)
    return render_template('login.html',
                           title='Create an Account.',
                           form=LoginForm(),
                           template='signup-page',
                           body="Sign up for a user account.")

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None
    
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))