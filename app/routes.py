from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from app.form import PersonForm
from app.models import Person, EmailReceiverModel
from app.utils import sendmail

main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route("/", methods=["GET", "POST"])
def home():
    person_form = PersonForm()

    if request.method == 'POST':
        data = request.form
        try:
            person_data = {}
            if data:
                for d in data:
                    print(d, data[d])
                    if hasattr(Person, d) and data[d] != '':
                        person_data[d] = data[d]

            # Convert Date string to python datetime object
            person_data['arrival_date'] = datetime.strptime(person_data['arrival_date'], '%Y-%m-%d').date()
            if 'departure_date' in person_data.keys():
                person_data['departure_date'] = datetime.strptime(person_data['departure_date'], '%Y-%m-%d').date()

            print(person_data)

            new_person = Person(**person_data)
            new_person.save_to_db()
            id = new_person.id_person
            print('<NEW PERSON ID>', id)

            recipients = EmailReceiverModel.query.all()
            for recipient in recipients:
                sendmail(recipient.subject, recipient.body, recipient.email, person_data)
            sendmail("Déclaration d'une nouvelle arrivée",
                     "Votre déclaration pour {} {} a bien été transmise. \n\n[Ceci est un message automatique]".format(
                         new_person.name, new_person.surname), new_person.email_referent, person_data)

        except Exception as e:
            print('ERROR', e)

        return redirect(url_for('main.person', id=id))

    return render_template("form.html", form=person_form)


@main_bp.route('/person/<int:id>')
def person(id):
    person = Person.query.filter_by(id_person=id).first()
    person_dict = dict((col, getattr(person, col)) for col in person.__table__.columns.keys())
    print('TYPE', type(person_dict))
    return render_template("person.html", person=person_dict)


@main_bp.route('/persons')
def persons():
    person = Person.query.all()
    persons_dict = []
    for p in person:
        p_dict = dict((col, getattr(p, col)) for col in p.__table__.columns.keys())
        persons_dict.append(p_dict)
    return render_template("persons.html", persons=persons_dict)


@main_bp.route('/recipients')
def recipients():
    recipients = EmailReceiverModel.query.all()
    recipients_dict = []
    for p in recipients:
        p_dict = dict((col, getattr(p, col)) for col in p.__table__.columns.keys())
        recipients_dict.append(p_dict)
    return render_template("recipients.html", recipients=recipients_dict)
