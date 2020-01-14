from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email
from app.utils import db
from wtforms.ext.sqlalchemy.orm import model_form, QuerySelectField
from wtforms.ext.sqlalchemy.fields import  QuerySelectField
from app.models import TerritoryUnit, PositionType, Person 

def get_territory_unit():
        return TerritoryUnit.query

def get_position_type():
        return PositionType.query

OldPersonForm = model_form(model=Person,
        base_class=FlaskForm,
        db_session=db.session)

class PersonForm(FlaskForm):        
    name = StringField('Nom', validators=[DataRequired()])
    surname = StringField('Prénom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    arrival_date = DateField('Date d\'arrivée', validators=[DataRequired()])
    departure_date = DateField('Date de départ')
    id_territory_unit = QuerySelectField('Unité territoriale', query_factory=get_territory_unit, get_label='name' )
    email_referent = StringField('Email responsable', validators=[DataRequired(), Email()])
    service = StringField('Service')
    workplace_address = TextAreaField('Addresse du lieu de travail')
    workplace_city = StringField('Ville du lieu de travail')
    phone_number = StringField('Numéro de téléphone')
    id_position_type = QuerySelectField('Type de position', query_factory=get_position_type, get_label='name')
    comment = TextAreaField('Commentaire')

    submit = SubmitField('Valider')