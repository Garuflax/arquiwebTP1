import os
import redis

from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail

ACCESS_EXPIRES = timedelta(minutes=15)
# Setup our redis connection for storing the blacklisted tokens
revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                      decode_responses=True)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'yeabackend.sqlite'),
    )
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    CORS(app)
    jwt = JWTManager(app)

    # Create our function to check if a token has been blacklisted. In this simple
    # case, we will just store the tokens jti (unique identifier) in redis
    # whenever we create a new token (with the revoked status being 'false'). This
    # function will return the revoked status of a token. If a token doesn't
    # exist in this store, we don't know where it came from (as we are adding newly
    # created tokens to our store with a revoked status of 'false'). In this case
    # we will consider the token to be revoked, for safety purposes.
    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decrypted_token):
        jti = decrypted_token['jti']
        entry = revoked_store.get(jti)
        return entry == 'true'


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