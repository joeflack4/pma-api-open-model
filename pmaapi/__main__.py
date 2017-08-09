#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entry point for package.

Some options for running:
 * gunicorn pmaapi.__main__:APP
<<<<<<< HEAD
 * gunicorn -b 0.0.0.0:<port> pmaapi.__main__:APP
    - port: Valid 4-digit port number, e.g. '8080'.
 * connexion run pmaapi/api.yaml -v
    - Assume app is structured such that this file is named 'api.py' and
      resides in same directory with 'api.yaml'.
 * <python> -m pmaapi
        - python: Your interpreter, e.g. python, python3, etc.
=======
    * Defaults to port 8000 on local, 8080 on Heroku.
 * gunicorn -b 0.0.0.0:<port> pmaapi.__main__:APP
    - Port: Valid 4-digit port number, e.g. '8080'.
 * connexion run pmaapi/api.yaml -v
    - Assume package is structured such that this file is named 'api.py' and
      resides in same directory with 'api.yaml'.
 * <python> -m pmaapi
    - Python: Your interpreter, e.g. python, python3, etc.
>>>>>>> develop
"""
import os
import sys
import connexion
from pmaapi.config import DevelopmentConfig
from werkzeug.utils import ImportStringError
from pmaapi.definitions.error import PmaApiException


def _configure(connexion_app):
    """Configure app.

    Args:
        connexion_app (ConnexionApp): Unconfigured Flask Connexion application.

    Returns:
        ConnexionApp: Configured Flask Connexion application.
    """
    # conf_app = app.add_api('api.yaml')  # TODO: Fix by conforming to spec.
    app = connexion_app.app  # To get to Flask app.

    try:
        app.config.from_object(os.environ['APP_SETTINGS'])
    except (KeyError, ModuleNotFoundError, ImportStringError):
        app.config.from_object(DevelopmentConfig)
    return connexion_app


def create_app():
    """Instantiate and configure app.

    Returns:
        ConnexionApp: Configured Connexion application. ConnexionApp.app is the
        Flask application.

    """
    # Ideally has: connexion.App(__name__, swagger_ui='docs'), but need to mess
    # with connexion in order to fix that.
    connexion_app = \
        _configure(connexion.App(__name__, specification_dir='api/'))
    return connexion_app


def run(server):
    """Run app.

    Args:
        server (ConnexionApp | FlaskApp): Configured application.

    Side effects:
        FlaskApp.run()
    """
<<<<<<< HEAD
    server.run(port=8000, debug=True)
=======
    server.run(port=8080, debug=True)
>>>>>>> develop


APP = create_app()
FLASK_APP = APP.app


if __name__ == '__main__':
    def create_db():
        """Create DB."""
        # from pmaapi.api.open_model.open_model_py.__main__ import db
        from flask_sqlalchemy import SQLAlchemy, declarative_base
        from pmaapi.api.open_model.open_model_py.__main__ import OpenModel
        from pmaapi.config import MODEL_FILE
        db = SQLAlchemy(FLASK_APP)
        db.Base = declarative_base()
        # TODO: Figure out how to get 'db' to know about this,
        #   if it doesn't automatically (reading from globals?).
        # models = OpenModel(MODEL_FILE)
        db.create_all()  # Run if it does not exist.
        db.session.commit()

    def test_db():
        """Test DB."""
        # - Test DB creation.
        # create_db()

        # - Test simple table manipulation.
        # from pmaapi.api.open_model.open_model_py.__main__ import add_module
        # some_data = {'name': 'test'}
        # add_module(db, some_data)

        # - Test Dynamic Class Generation
        #   Instance Variables
        # from pmaapi.api.open_model.open_model_py.__main__ import AllMyFields
        # class_gen = AllMyFields({'a': 1, 'b': 2})
        # print(class_gen.a)
        #   Entire Class
        # my_class = type('MyClass', (object,),
        #                 {'hello_world': lambda x: 'hello'})
        # my_instance = my_class()
        # print(my_instance.hello_world())

        # - Test SqlAlchemy Table Autogeneration
        # from sqlalchemy import Column, Integer
        # from pmaapi.api.open_model.open_model_py.__main__ import db
        # table_class_def = {
        #     '__tablename__': 'example_table',
        #     'id': Column(Integer, primary_key=True)
        # }
        #
        # # noinspection PyUnusedLocal
        # example_table_class = type(
        #     'ExampleTableClass', (db.Model,), table_class_def
        # )
        # db.create_all()  # Run if it does not exist.
        # db.session.commit()

        # - Test OpenModel
        from pmaapi.api.open_model.open_model_py.__main__ import OpenModel, \
            MODEL_FILE
        mdl = OpenModel()
        mdl.load(MODEL_FILE)
        create_db()

        pass
    try:
        test_db()
        # run(app)
    except PmaApiException as err:
        print(err, file=sys.stderr)
