from flask import Flask, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user, login_user
from flask_migrate import Migrate
from app.oauth import OAuthSignIn

from config import app_config

db = SQLAlchemy()
lm = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)

    lm.init_app(app)
    lm.login_message = "You must be logged in to access this message"
    lm.login_view = "auth.login"

    migrate = Migrate(app, db)
    from app.models import Customer


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/authorize/<provider>')
    def oauth_authorize(provider):
        if not current_user.is_anonymous:
            return redirect(url_for('index'))
        oauth = OAuthSignIn.get_provider(provider)
        return oauth.authorize()

    @app.route('/callback/<provider>')
    def oauth_callback(provider):
        if not current_user.is_anonymous:
            return redirect(url_for('index'))
        oauth = OAuthSignIn.get_provider(provider)
        social_id, username, email = oauth.callback()
        if social_id is None:
            flash('Authentication failed.')
            return redirect(url_for('index'))
        user = Customer.query.filter_by(social_id=social_id).first()
        if not user:
            user = Customer(social_id=social_id, nickname=username, email=email)
            db.session.add(user)
            db.session.commit()
        login_user(user, True)
        return redirect(url_for('index'))

    return app