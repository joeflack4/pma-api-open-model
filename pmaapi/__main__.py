#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entry point for package.

Some options for running:
 * gunicorn pmaapi.__main__:APP
    * Defaults to port 8000 on local, 8080 on Heroku.
 * gunicorn -b 0.0.0.0:<port> pmaapi.__main__:APP
    - Port: Valid 4-digit port number, e.g. '8080'.
 * connexion run pmaapi/api.yaml -v
    - Assume package is structured such that this file is named 'api.py' and
      resides in same directory with 'api.yaml'.
 * <python> -m pmaapi
    - Python: Your interpreter, e.g. python, python3, etc.
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
    server.run(port=8080, debug=True)


APP = create_app()
FLASK_APP = APP.app


if __name__ == '__main__':
    def test_db():
        """Test DB."""
        from pmaapi.api.open_model.open_model_py.__main__ import db, add_module
        db.create_all()
        db.session.commit()

        some_data = {'name': 'test'}
        add_module(db, some_data)
    try:
        test_db()
        # run(app)
    except PmaApiException as err:
        print(err, file=sys.stderr)
