from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.fields import DateField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email

from app.models import TerritoryUnit, PositionType, ContractType, TeamsList

common_input = {"class": "form-control"}
datepicker = {"class": "form-control datepicker"}
big_textarea_input = common_input.copy()
big_textarea_input["rows"] = 20


def get_territory_unit():
    return TerritoryUnit.query


def get_position_type():
    return PositionType.query


def get_contract_type():
    return ContractType.query


def get_teams_list():
    return TeamsList.query


class PersonForm(FlaskForm):
    email_declarator = EmailField(
        "Votre email (pour envoi d'une confirmation)",
        validators=[DataRequired(), Email()],
        render_kw=common_input,
    )
    name = StringField("Nom", validators=[DataRequired()], render_kw=common_input)
    surname = StringField("Prénom", validators=[DataRequired()], render_kw=common_input)
    email = EmailField(
        "Email", validators=[DataRequired(), Email()], render_kw=common_input
    )
    arrival_date = DateField(
        "Date d'arrivée", validators=[DataRequired()], render_kw=datepicker
    )
    departure_date = DateField("Date de départ", render_kw=datepicker)
    territory_unit = QuerySelectField(
        "Délégation territoriale",
        validators=[DataRequired()],
        query_factory=get_territory_unit,
        get_label="name",
        get_pk=lambda a: a.name,
        render_kw=common_input,
    )
    email_referent = EmailField(
        "Email du responsable",
        validators=[DataRequired(), Email()],
        render_kw=common_input,
    )
    service = StringField("Service/Pôle", render_kw=common_input)
    workplace_address = TextAreaField(
        "Adresse du lieu de travail",
        validators=[DataRequired()],
        render_kw=common_input,
    )
    workplace_city = StringField(
        "Ville du lieu de travail", validators=[DataRequired()], render_kw=common_input
    )
    phone_number = StringField(
        "Numéro de téléphone", validators=[DataRequired()], render_kw=common_input
    )
    contract_type = QuerySelectField(
        "Type de contrat",
        validators=[DataRequired()],
        query_factory=get_contract_type,
        get_label="name",
        get_pk=lambda a: a.name,
        render_kw=common_input,
    )
    position_type = QuerySelectField(
        "Type de poste",
        validators=[DataRequired()],
        query_factory=get_position_type,
        get_label="name",
        get_pk=lambda a: a.name,
        render_kw=common_input,
    )
    teams_list = QuerySelectMultipleField(
        "Selectionnez les listes de diffusion mail auxquelles la personne doit être rattachée",
        query_factory=get_teams_list,
        get_label="name",
        get_pk=lambda a: a.name,
        render_kw=common_input,
    )
    comment = TextAreaField(
        "Commentaire",
        render_kw=common_input,
        description="<b>Si vous avez besoin d'une ligne mobile</b>, merci de le préciser",
    )


class RecipientForm(FlaskForm):
    email = EmailField(
        "Email du destinataire",
        validators=[DataRequired(), Email()],
        render_kw=common_input,
    )
    subject = StringField(
        "Subject", validators=[DataRequired()], render_kw=common_input
    )
    body = TextAreaField(
        "Corps de texte", validators=[DataRequired()], render_kw=big_textarea_input
    )
