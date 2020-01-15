from pathlib import Path
import os
from app import conf
from flask import Flask
from app.routes import main_bp
from app.utils import db, migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import MenuLink
from flask import url_for



def create_app():
    app = Flask(__name__)
    app.config.from_object(conf)

    with Path(__file__).parent.parent as root_dir:
        database_file = "sqlite:///{}".format(os.path.join(root_dir, app.config["DB_FILE_NAME"]))
        print('<DB FILE : {}>'.format(database_file))
        app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp, url_prefix="/")

    admin = Admin(app, name='AutoMailSender', template_mode='bootstrap3')

    from app.models import TerritoryUnit, PositionType,Person, Recipient, RecipientAdmin, PersonAdmin
    admin.add_view(PersonAdmin(Person, db.session))
    admin.add_view(ModelView(TerritoryUnit, db.session))
    admin.add_view(ModelView(PositionType, db.session))
    admin.add_view(RecipientAdmin(Recipient, db.session))
    admin.add_link(MenuLink(name='Site publique', category='', url='/'))
    


    with app.app_context():
        db.create_all()

    return app


app = create_app()
