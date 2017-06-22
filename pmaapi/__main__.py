"""Entry point for package."""
import connexion


def configuration():
    """Configure app.

    Returns:
        FlaskApp: Configured Flask application.
    """
    # Ideally has: connexion.App(__name__, swagger_ui='docs')
    app = connexion.App(__name__, specification_dir='spec/')
    app.add_api('api.yaml')
    return app


def run(app):
    """Run app.

    Args:
        app (FlaskApp): Configured Flask application.

    Side effects: app.run()
    """
    app.run(port=8080)


if __name__ == '__main__':
    run(configuration())
