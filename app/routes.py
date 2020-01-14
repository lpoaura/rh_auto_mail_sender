from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.form import PersonForm, RecipientForm
from app.models import Person, Recipient
from app.utils import sendmail

main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@main_bp.route("/person/add", methods=["GET", "POST"])
def person_add():
    person_form = PersonForm()

    if request.method == 'POST':
        data = request.form
        try:
            person_data = {}
            if data:
                for d in data:
                    # print(d, data[d])
                    if hasattr(Person, d) and data[d] != '':
                        person_data[d] = data[d]

            # Convert Date string to python datetime object
            person_data['arrival_date'] = datetime.strptime(person_data['arrival_date'], '%Y-%m-%d').date()
            if 'departure_date' in person_data.keys():
                person_data['departure_date'] = datetime.strptime(person_data['departure_date'], '%Y-%m-%d').date()

            new_person = Person(**person_data)
            new_person.save_to_db()
            id = new_person.id_person
            print('<person_add id>', id)
            flash('Merci pour cette participation')
            recipient_list = Recipient.query.all()
            for recipient in recipient_list:
                sendmail(recipient.subject, recipient.body, recipient.email, person_data)

        except Exception as e:
            flash(e)
            print("<person_add error>", e)
            return render_template("person_form.html", form=person_form)

        return redirect(url_for('main.person', id=id))

    return render_template("person_form.html", form=person_form)


@main_bp.route('/person/<int:id>')
def person(id):
    pers = Person.query.filter_by(id_person=id).first()
    person_dict = dict((col, getattr(pers, col)) for col in pers.__table__.columns.keys())
    print('TYPE', type(person_dict))
    return render_template("person.html", person=person_dict)


@main_bp.route('/persons')
def persons():
    try:
        pers = Person.query.all()
        persons_dict = []
        for p in pers:
            p_dict = dict((col, getattr(p, col)) for col in p.__table__.columns.keys())
            persons_dict.append(p_dict)
        return render_template("persons.html", persons=persons_dict)
    except Exception as e:
        flash('Aucune donnée')
        print("<persons error>", e)
        return render_template("problem.html")


@main_bp.route("/recipient/add", methods=["GET", "POST"])
def add_recipient():
    recipient_form = RecipientForm()

    if request.method == 'POST':
        data = request.form
        try:
            recipient_data = {}
            if data:
                for d in data:
                    print(d, data[d])
                    if hasattr(Recipient, d):
                        recipient_data[d] = data[d]

            new_recipient = Recipient(**recipient_data)
            new_recipient.save_to_db()

        except Exception as e:
            print("<add_recipient error>", e)
            flash(e)
            return render_template("recipient_form.html", form=recipient_form)

        return redirect(url_for('main.recipients'))

    return render_template("recipient_form.html", form=recipient_form)


@main_bp.route('/recipients')
def recipients():
    try:
        recipients = Recipient.query.all()
        recipients_dict = []
        for p in recipients:
            p_dict = dict((col, getattr(p, col)) for col in p.__table__.columns.keys())
            recipients_dict.append(p_dict)
        return render_template("recipients.html", recipients=recipients_dict)
    except Exception as e:
        print("<recipients error>", e)
        return render_template("problem.html")
