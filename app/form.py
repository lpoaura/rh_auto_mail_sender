from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email

from app.models import TerritoryUnit, PositionType

common_input = {'class': 'form-control'}
datepicker = {'class': 'form-control datepicker'}


def get_territory_unit():
    return TerritoryUnit.query


def get_position_type():
    return PositionType.query


class PersonForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()], render_kw=common_input)
    surname = StringField('Prénom', validators=[DataRequired()], render_kw=common_input)
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw=common_input)
    arrival_date = DateField('Date d\'arrivée', validators=[DataRequired()], render_kw=datepicker)
    departure_date = DateField('Date de départ', render_kw=datepicker)
    territory_unit_id = QuerySelectField('Délégation territoriale', validators=[DataRequired()], query_factory=get_territory_unit, get_label='name',
                                         get_pk=lambda a: a.id_territory_unit,
                                         render_kw=common_input)
    email_referent = StringField('Email responsable', validators=[DataRequired(), Email()], render_kw=common_input)
    service = StringField('Service', render_kw=common_input)
    workplace_address = TextAreaField('Addresse du lieu de travail', validators=[DataRequired()], render_kw=common_input)
    workplace_city = StringField('Ville du lieu de travail', validators=[DataRequired()],  render_kw=common_input)
    phone_number = StringField('Numéro de téléphone', render_kw=common_input)
    position_type_id = QuerySelectField('Type de poste', validators=[DataRequired()], query_factory=get_position_type, get_label='name',
                                        get_pk=lambda a: a.id_position_type,
                                        render_kw=common_input)
    comment = TextAreaField('Commentaire', render_kw=common_input)


class RecipientForm(FlaskForm):
    email = StringField('Email du destinataire', validators=[DataRequired(), Email()], render_kw=common_input)
    subject = StringField('Subject', validators=[DataRequired()], render_kw=common_input)
    body = TextAreaField('Corps de texte', validators=[DataRequired()], render_kw=common_input)
