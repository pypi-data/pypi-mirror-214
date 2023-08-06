import glob
import os
import sys
from datetime import datetime
import logging
import getpass

import toml

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_login import LoginManager

from photoflow.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from photoflow.extensions import db, login_manager, migrate

logging.basicConfig(level=logging.INFO)


class SchemeFromProxy:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        WTF_CSRF_SECRET_KEY='dev',
        PUBLIC_ON_HOME=False,
        SEND_FILE_MAX_AGE_DEFAULT=60,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///database.db',
    )

    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_pyfile('config.py', silent=True)
    app.config.from_file('config.toml', load=toml.load, silent=True)

    app.wsgi_app = SchemeFromProxy(app.wsgi_app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from photoflow.importer import import_image, check_file_supported, remove_missing_from_datastore

    from photoflow import models
    from photoflow.frontend.authentication import blueprint_auth
    from photoflow.frontend.home import blueprint_home
    from photoflow.frontend.image import blueprint_image
    from photoflow.frontend.picture import blueprint_picture
    from photoflow.frontend.album import blueprint_album
    from photoflow.frontend.upload import blueprint_upload
    from photoflow.frontend.piwigo import blueprint_piwigo

    app.register_blueprint(blueprint_auth)
    app.register_blueprint(blueprint_home)
    app.register_blueprint(blueprint_image)
    app.register_blueprint(blueprint_picture)
    app.register_blueprint(blueprint_album)
    app.register_blueprint(blueprint_upload)
    app.register_blueprint(blueprint_piwigo)


    @login_manager.user_loader
    def load_user(user_id):
        return models.User.get(user_id)


    @app.cli.command('create-user')
    @click.argument("username")
    @click.option("--admin/--no-admin", default=False)
    @with_appcontext
    def create_user(username, admin):
        password = getpass.getpass()
        if not password:
            print("Password cannot be empty")
            exit(1)
        user = models.User()
        user.username = username
        user.is_admin = admin
        user.created = datetime.now()
        user.set_password(password)
        db.session.add(user)
        db.session.commit()


    @app.cli.command('import-image')
    @click.argument("path", nargs=-1)
    @with_appcontext
    def import_path(path):
        for name in path:
            for img in glob.glob(name, recursive=True):
                if check_file_supported(img):
                    print(f"Importing {img}...")
                    import_image(img)
                else:
                    print(f"Skipping {img}")
        print("Done")


    @app.cli.command('clean-database')
    @with_appcontext
    def clean_database():
        remove_missing_from_datastore()

    return app
