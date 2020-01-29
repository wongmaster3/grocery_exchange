from flask import Flask, render_template

from grocery.models import db, Exchange
from . import config
from grocery.auth.forms import LoginForm, RegisterForm
from flask_login import LoginManager
import os
import pytesseract as pytess

app = Flask(__name__)
login_manager = LoginManager()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
pytess.pytesseract.tesseract_cmd = os.path.abspath(os.getcwd()) + '/tesseract'

def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super secret key'
    app.config['UPLOAD_FOLDER'] = os.path.abspath(os.getcwd()) + '/receipts'

    app.app_context().push()
    db.init_app(app)

    # Register the blueprints
    from grocery.auth.routes import auth
    from grocery.exchange.routes import exchange

    app.register_blueprint(auth)
    app.register_blueprint(exchange)

    # Initialize the transaction loader
    @login_manager.user_loader
    def load_user(user_id):
        return Exchange.query.get(user_id)

    # Initialize login manager
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Initialize the navigation bar
    # from grocery.navigation import account_nav

    # Login page will be the home page
    @app.route('/')
    def index():
        return render_template("login.html", formlog = LoginForm(), formreg = RegisterForm())

    return app

if __name__ == "__main__":
    app.run(threaded=True)

