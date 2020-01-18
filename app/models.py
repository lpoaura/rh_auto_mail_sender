from datetime import datetime

from flask_admin.contrib.sqla import ModelView

from app.utils import db, SaveMixin


class TerritoryUnit(db.Model, SaveMixin):
    id_territory_unit = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)


class PositionType(db.Model, SaveMixin):
    id_position_type = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)


class ContractType(db.Model, SaveMixin):
    id_contract_type = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)


class TeamsList(db.Model, SaveMixin):
    id_contract_type = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)


class Recipient(db.Model, SaveMixin):
    id_email_received_model = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)
    create_ts = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return "<EmailReceiverModel: {} {}>".format(self.email, self.subject)


class RecipientAdmin(ModelView):
    form_widget_args = {
        'body': {
            'rows': 20
        }
    }


class Person(db.Model, SaveMixin):
    id_person = db.Column(db.Integer, primary_key=True)
    email_declarator = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=True)
    territory_unit = db.Column(db.String(256), db.ForeignKey('territory_unit.name'), nullable=False)
    email_referent = db.Column(db.String(256), nullable=False)
    service = db.Column(db.String(256), nullable=True)
    workplace_address = db.Column(db.String(1000), nullable=True)
    workplace_city = db.Column(db.String(256), nullable=True)
    phone_number = db.Column(db.String(256), nullable=False)
    contract_type = db.Column(db.String(256), db.ForeignKey('contract_type.name'), nullable=False)
    position_type = db.Column(db.String(256), db.ForeignKey('position_type.name'), nullable=False)
    job_title = db.Column(db.String(256), nullable=True)
    teams_list = db.Column(db.String(1000), nullable=True)
    comment = db.Column(db.String(), nullable=True)
    create_ts = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return "<PersonModel: {} {}>".format(self.name, self.surname)

    def fullname(self):
        return "{} {}".format(self.name, self.username)


class PersonAdmin(ModelView):
    can_create = False
