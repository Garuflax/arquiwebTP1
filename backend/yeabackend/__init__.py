import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'yeabackend.sqlite'),
    )
    CORS(app)
    JWTManager(app)


    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = 'yo.estuve.aqui.app@gmail.com'
    app.config["MAIL_PASSWORD"] = 'A.12345678'

    mail = Mail()
    mail.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello TODO: change for client at index.html
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import location
    app.register_blueprint(location.bp)

    from . import check
    app.register_blueprint(check.bp)

    from . import data
    app.register_blueprint(data.bp)

    from . import inform
    app.register_blueprint(inform.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    return app