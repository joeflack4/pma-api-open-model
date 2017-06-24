"""App entry point for Heroku."""
from pmaapi.__main__ import configuration, run


app = configuration()

if __name__ == '__main__':
    run(configuration())
