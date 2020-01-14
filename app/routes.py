from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Person
from app.utils import db
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from app.form import PersonForm

main_bp = Blueprint('mail', __name__, template_folder='templates')


@main_bp.route("/", defaults={'id': None}, methods=["GET", "POST"])
@main_bp.route("/person/<int:id>", methods=["GET", "POST"])
def home(id=None):
    person_form = PersonForm()
    
    if id == None:
        person = Person()
    else:
        person = Person.query.get(id)

    if person_form.validate_on_submit():
            new_person = person_form.populate_obj(person)
            db.session.add(new_person)
            db.session.commit()
            flash("yay!")

    # if request.method == 'POST':
    #     data = request.form
    #     try:
    #         person_data = {}
    #         if data:
    #             for d in data:
    #                 print(d, data[d])
    #                 if hasattr(Person, d):
    #                     person_data[d] = data[d]
    #         new_person = Person(**person_data)
    #         new_person.save_to_db()
    #         id = new_person.id_person
    #         print('<NEW PERSON ID>', id)
    #     except Exception as e:
    #         print('ERROR',e)

        # return redirect(url_for('person', id=id))

    return render_template("form.html", form=person_form)


@main_bp.route('/person/<int:id>')
def person(id):
    person = Person.query.filter(id_person=id)
    return 'Hello, {}'.format(person.fullname())
