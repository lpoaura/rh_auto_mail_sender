from datetime import datetime
import config

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
    id_teams_list = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)


class Recipient(db.Model, SaveMixin):
    id_email_received_model = db.Column(db.Integer, primary_key=True)
    dest_type = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)
    create_ts = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return "<EmailReceiverModel: {} {}>".format(self.email, self.subject)


class RecipientAdmin(ModelView):
    form_widget_args = {
        "body": {"rows": 20},
    }
    form_choices = {"dest_type": [(t, t) for t in config.TYPE_DEST]}


class Person(db.Model, SaveMixin):
    id_person = db.Column(db.Integer, primary_key=True, doc="ID de la donnée")
    email_declarator = db.Column(
        db.String(256), nullable=False, doc="Email du déclarant"
    )
    name = db.Column(db.String(80), nullable=False, doc="Nom")
    surname = db.Column(db.String(80), nullable=False, doc="Prénom")
    email = db.Column(db.String(256), nullable=False, doc="Email")
    arrival_date = db.Column(db.Date, nullable=False, doc="Date d'arrivée")
    departure_date = db.Column(db.Date, nullable=True, doc="Date de départ")
    territory_unit = db.Column(
        db.String(256),
        db.ForeignKey("territory_unit.name"),
        nullable=False,
        doc="Délégation territoriale",
    )
    email_referent = db.Column(
        db.String(256), nullable=False, doc="Email du responsable"
    )
    service = db.Column(db.String(256), nullable=True, doc="Service de rattachement")
    workplace_address = db.Column(
        db.String(1000), nullable=True, doc="Adresse du lieu de travail"
    )
    workplace_city = db.Column(
        db.String(256), nullable=True, doc="Ville du lieu de travail"
    )
    phone_number = db.Column(db.String(256), nullable=False, doc="Numéro de téléphone")
    contract_type = db.Column(
        db.String(256),
        db.ForeignKey("contract_type.name"),
        nullable=False,
        doc="Type de contrat",
    )
    position_type = db.Column(
        db.String(256),
        db.ForeignKey("position_type.name"),
        nullable=False,
        doc="Type de poste",
    )
    job_title = db.Column(db.String(256), nullable=True, doc="Intitulé du poste")
    teams_list = db.Column(db.String(1000), nullable=True, doc="Listes TEAMS")
    comment = db.Column(db.String(), nullable=True, doc="Commentaire")
    create_ts = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(),
        doc="Date/heure de création de la donnée",
    )

    def __repr__(self):
        return "<PersonModel: {} {}>".format(self.name, self.surname)

    def fullname(self):
        return "{} {}".format(self.name, self.username)


class PersonAdmin(ModelView):
    can_create = False
