from datetime import datetime

from app.utils import db, SaveMixin
from flask_admin.contrib.sqla import ModelView


class TerritoryUnit(db.Model, SaveMixin):
    id_territory_unit = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)


class PositionType(db.Model, SaveMixin):
    id_position_type = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)


class EmailReceiverModel(db.Model, SaveMixin):
    id_email_received_model = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<EmailReceiverModel: {} {}>".format(self.email, self.subject)

class EmailReceiverAdmin(ModelView):
    form_widget_args = {
        'body': {
            'rows': 20
        }
    }

class Person(db.Model, SaveMixin):
    id_person = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=True)
    territory_unit_id = db.Column(db.Integer(), db.ForeignKey('territory_unit.id_territory_unit'), nullable=False)
    email_referent = db.Column(db.String(256), nullable=False)
    service = db.Column(db.String(256), nullable=True)
    workplace_address = db.Column(db.String(1000), nullable=True)
    workplace_city = db.Column(db.String(256), nullable=True)
    phone_number = db.Column(db.String(256), nullable=False)
    position_type_id = db.Column(db.Integer(), db.ForeignKey('position_type.id_position_type'), nullable=False)
    job_title = db.Column(db.String(256), nullable=True)
    comment = db.Column(db.String(), nullable=True)
    create_ts = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return "<PersonModel: {} {}>".format(self.name, self.surname)

    def fullname(self):
        return "{} {}".format(self.name, self.username)

class PersonAdmin(ModelView):
    can_create=False