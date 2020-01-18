import os
from pathlib import Path

from flask import Flask
from flask_admin import Admin
from flask_admin.base import MenuLink
from flask_admin.contrib.sqla import ModelView

from app import conf
from app.routes import main_bp
from app.utils import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(conf)

    with Path(__file__).parent.parent as root_dir:
        database_file = "sqlite:///{}".format(os.path.join(root_dir, 'db.sqlite'))
        print('<DB FILE : {}>'.format(database_file))
        app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp, url_prefix="/")

    admin = Admin(app, name=app.config["APP_NAME"], template_mode='bootstrap3')

    from app.models import TerritoryUnit, PositionType, Person, Recipient, RecipientAdmin, PersonAdmin, ContractType, \
        TeamsList
    admin.add_link(MenuLink(name='Site publique', category='', url='/'))
    admin.add_view(PersonAdmin(Person, db.session, name='Personnes déclarées'))
    admin.add_view(ModelView(TerritoryUnit, db.session, name='Délégations'))
    admin.add_view(ModelView(ContractType, db.session, name='Contrats'))
    admin.add_view(ModelView(PositionType, db.session, name='Postes'))
    admin.add_view(ModelView(TeamsList, db.session, name='Listes teams'))
    admin.add_view(RecipientAdmin(Recipient, db.session, name='Destinataires'))

    with app.app_context():
        db.create_all()

    return app


app = create_app()
