from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email
from app.utils import db
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import TerritoryUnit, PositionType, Person

common_input = {'class': 'form-control'}
datepicker = {'class': 'form-control datepicker'}


def get_territory_unit():
    return TerritoryUnit.query


def get_position_type():
    return PositionType.query


OldPersonForm = model_form(model=Person,
                           base_class=FlaskForm,
                           db_session=db.session)


class PersonForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()], render_kw=common_input)
    surname = StringField('Prénom', validators=[DataRequired()], render_kw=common_input)
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw=common_input)
    arrival_date = DateField('Date d\'arrivée', validators=[DataRequired()], render_kw=datepicker)
    departure_date = DateField('Date de départ', render_kw=datepicker)
    territory_unit_id = QuerySelectField('Délégation territoriale', query_factory=get_territory_unit, get_label='name',
                                         get_pk=lambda a: a.id_territory_unit,
                                         render_kw=common_input)
    email_referent = StringField('Email responsable', validators=[DataRequired(), Email()], render_kw=common_input)
    service = StringField('Service', render_kw=common_input)
    workplace_address = TextAreaField('Addresse du lieu de travail', render_kw=common_input)
    workplace_city = StringField('Ville du lieu de travail', render_kw=common_input)
    phone_number = StringField('Numéro de téléphone', render_kw=common_input)
    position_type_id = QuerySelectField('Type de poste', query_factory=get_position_type, get_label='name',
                                        get_pk=lambda a: a.id_position_type,
                                        render_kw=common_input)
    comment = TextAreaField('Commentaire', render_kw=common_input)

    # submit = SubmitField('Valider')
