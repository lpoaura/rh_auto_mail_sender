from app import app
from werkzeug.debug import DebuggedApplication
from app.utils import GunicornApp
import logging
import os


def run_gunicorn_app(host, port, debug, **settings):
    """Serve Flask application using Gunicorn.
    The Flask application and respective resources and endpoints should
    defined in `app.py` in this same directory.
    """

    logging.basicConfig(level='DEBUG' if debug else 'INFO')

    # Set a global flag that indicates that we were invoked from the
    # command line interface provided server command.  This is detected
    # by Flask.run to make the call into a no-op.  This is necessary to
    # avoid ugly errors when the script that is loaded here also attempts
    # to start a server.
    os.environ['FLASK_RUN_FROM_CLI_SERVER'] = '1'

    settings['bind'] = '{}:{}'.format(host, port)

    if debug:
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        settings.update({'loglevel': 'debug',
                         'reload': True,
                         'threads': 1,
                         'workers': 1,
                         'worker_class': 'sync'})
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
        logging.info(" * Launching in Debug mode.")
        logging.info(" * Serving application using a single worker.")
    else:
        logging.info(" * Launching in Production Mode.")
        logging.info(" * Serving application with {} worker(s)."
                     .format(settings["workers"]))

    server = GunicornApp(app, settings=settings)
    server.run()


if __name__ == '__main__':
    run_gunicorn_app(host='0.0.0.0', port=5555, debug=True)
