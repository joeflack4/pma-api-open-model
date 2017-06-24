"""Entry point for package.

Some options for running:
 * gunicorn pmaapi.__main__:APP
 * gunicorn -b 0.0.0.0:<port> pmaapi.__main__:APP
    - port: Valid 4-digit port number, e.g. '8080'.
 * connexion run pmaapi/api.yaml -v
    - Assume app is structured such that this file is named 'api.py' and
      resides in same directory with 'api.yaml'.
 * <python> -m pmaapi
        - python: Your interpreter, e.g. python, python3, etc.
"""
import connexion


def configuration():
    """Configure app.

    Returns:
        FlaskApp: Configured Flask application.

    """
    # Ideally has: connexion.App(__name__, swagger_ui='docs')
    flask_connexion_app = connexion.App(__name__, specification_dir='spec/')
    flask_connexion_app.add_api('api.yaml')
    return flask_connexion_app


def run(server):
    """Run app.

    Args:
        server (FlaskApp): Configured Flask application.

    Side effects:
        server.run()
    """
    server.run(port=8000, debug=True)


APP = configuration()

if __name__ == '__main__':
    run(configuration())
