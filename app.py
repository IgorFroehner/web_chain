from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from decouple import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = config('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)


def register_routes(app):
    from routes import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    return app


app = register_routes(app)
