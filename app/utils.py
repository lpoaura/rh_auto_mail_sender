import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from gunicorn.app.base import BaseApplication

import config

migrate = Migrate()

db = SQLAlchemy()


def version():
    """Return SITE VERSION to frontend"""
    with open("VERSION", "r") as VERSION:
        version = VERSION.read().replace("\n", "n")
        return version


class SaveMixin(object):
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class GunicornApp(BaseApplication):
    """Convert a Flask application to a Gunicorn one.
    """

    def __init__(self, flask_app, settings=None):
        """Initialize GunicornApp.
        If no settings are provided the class is initialized using the
        documented default parameters in
        http://docs.gunicorn.org/en/stable/settings.html#config-file.
        Args:
            flask_app (flask.app.Flask): Application to be wrapped by
                gunicorn.
            settings (dict): Settings defining the configuration to use
                when lounching the gunicorn application. If any setting
                is missing, the corresponding the default value is used.
        """
        self.flask_app = flask_app
        self.settings = settings or {}
        super().__init__()

    def load_config(self):
        """Update application configuration with given parameters.
        We update element by element intead of using dict.update()
        because we want the method to fail if a setting was given in
        the __init__ which does not exist or it is misspelled.
        """
        for k, v in self.settings.items():
            self.cfg.set(k, v)

    def load(self):
        return self.flask_app


def sendmail(subject, body, recipient, datas):
    try:
        pre_title = subject.format(**datas)
        title = "[{app_name}] {subject}".format(app_name=config.APP_NAME, subject=pre_title)
        body = body.format(**datas)
        print('content', body)

        msg = MIMEMultipart()
        msg['reply-to'] = datas['email_declarator']
        msg['From'] = config.SMTP_LOGIN
        msg['To'] = recipient
        msg['Subject'] = title
        message = MIMEText(body)
        msg.attach(message)

        # message = 'Subject: {subject}\n\n{body}'.format(subject=title, body=body)

        print('<MESSAGE>', msg)

        mailserver = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(config.SMTP_LOGIN, config.SMTP_PWD)
        mailserver.send_message(msg)
        mailserver.quit()
    except Exception as e:
        print('<sendmail() error> {}'.format(e))
