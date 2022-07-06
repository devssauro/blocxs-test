# from flask import Flask
from apiflask import APIFlask
from db_config import db, migrate
from . import config


def create_app(test_config=None):
    app = APIFlask(__name__, instance_relative_config=True, )
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.get('/')
    def hello():
        return 'hello'

    # @app.before_first_request
    # def create_users():
    #     pass

    # @user_confirmed.connect_via(app)
    # def _user_confirmed(sender, user):
    #     pass

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import mod_auth
    app.register_blueprint(mod_auth.bp())
    from . import mod_account
    app.register_blueprint(mod_account.bp())

    return app
