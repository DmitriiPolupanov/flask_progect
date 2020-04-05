from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_path='%s\\flask_web_app' % os.getcwd())
    app.config.update(SECRET_KEY = 'secret_xxx', SQLALCHEMY_DATABASE_URI = 'sqlite:///db/webapp.db')
    app.jinja_env.add_extension('jinja2.ext.do')
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth

        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
        
        db.create_all()
        return app



