from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Person
from app.utils import db
from sqlalchemy.exc import IntegrityError

main_bp = Blueprint('mail', __name__, template_folder='templates')


@main_bp.route("/", methods=["GET", "POST"])
def home():
    data = request.form
    if request.method == 'POST':
        try:
            person_data = {}
            if data:
                for d in data:
                    print(d, data[d])
                    if hasattr(Person, d):
                        person_data[d] = data[d]
            new_person = Person(**person_data)
            new_person.save_to_db()
            id = new_person.id_person
            print('<NEW PERSON ID>', id)
        except Exception as e:
            print('ERROR',e)

        # return redirect(url_for('person', id=id))

    return render_template("form.html")


@main_bp.route('/person/<int:id>')
def person(id):
    person = Person.query.filter(id_person=id)
    return 'Hello, {}'.format(person.fullname())
