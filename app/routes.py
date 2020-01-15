from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash

import config
from app.form import PersonForm, RecipientForm, str_to_class
from app.models import Person, Recipient, FormFields, PersonJson
from app.utils import sendmail, version

main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.context_processor
def global_variables():
    values = {}
    values["app_name"] = config.APP_NAME
    values["version"] = version()
    return values


@main_bp.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@main_bp.route("/person/add", methods=["GET", "POST"])
def person_add():
    person_form = PersonForm()
    recipient_list = Recipient.query.all()
    print('<person_add Method>', request.method)
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

            new_person = Person(**person_data)
            new_person.save_to_db()
            id = new_person.id_person
            print('<person_add id>', id)
            print('<person_row>', new_person)

            flash('Merci pour cette participation')

            new_person_dict = dict((col, getattr(new_person, col)) for col in new_person.__table__.columns.keys())
            print('<new_person_dict 1>', type(new_person_dict), new_person_dict)

            for k, v in new_person_dict.items():
                print(k, v)
                if new_person_dict[k] == None:
                    print(k)
                    new_person_dict[k] = 'Non défini'

            print('<new_person_dict 2>', new_person_dict)

            for recipient in recipient_list:
                sendmail(recipient.subject, recipient.body, recipient.email, new_person_dict)
            sendmail("Déclaration d'une nouvelle arrivée",
                     "Votre déclaration pour {} {} a bien été transmise. \n\n[Ceci est un message automatique]".format(
                         new_person.name, new_person.surname), new_person.email_referent, person_data)

        except Exception as e:
            flash(e)
            print("<person_add error>", e)
            return render_template("person_form.html", form=person_form, recipients=recipient_list)

        return redirect(url_for('main.person', id=id))

    return render_template("person_form.html", form=person_form, recipients=recipient_list)


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
def recipient_add():
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

        return redirect(url_for('main.recipients_list'))

    return render_template("recipient_form.html", form=recipient_form)


@main_bp.route('/recipients')
def recipients_list():
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


@main_bp.route('/testform', methods=["GET", "POST"])
def test_form():
    recipient_list = Recipient.query.all()
    try:
        form_fields = FormFields.query.all()

        from flask_wtf import FlaskForm

        class F(FlaskForm):
            pass

        common_input = {'class': 'form-control'}
        for field in form_fields:
            field_class = common_input.copy()

            print('field.field_class', field.field_class)
            if field.field_class is not None:
                field_class['class'] = '{} {}'.format(common_input['class'], field.field_class)
                print(field_class)
            setattr(F, field.field_name, str_to_class(field.field_type)(field.field_label, render_kw=field_class))

        if request.method == 'POST':
            data = request.form
            print(data)
            try:
                data_dict = {}
                if data:
                    for d in data:
                        print(data[d], d)
                        if d != 'csrf_token':
                            data_dict[d] = data[d]
                            print('<test_form post result>', data_dict)

                new_person = PersonJson()
                new_person.json_data = data_dict
                new_person.save_to_db()
                print('<new_person_json>', new_person.id_person_json)

            except Exception as e:
                print('<error testform result>', e)




    except Exception as e:
        print('<error test_form>', e)

    return render_template("test_form.html", form=F(), recipients=recipient_list)
