from app.utils import db, SaveMixin


class Person(db.Model, SaveMixin):
    id_person = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=True)
    department = db.Column(db.String(256), nullable=False)
    email_referent = db.Column(db.String(256), nullable=False)
    service = db.Column(db.String(256), nullable=True)
    workplace_address = db.Column(db.String(1000), nullable=True)
    workplace_city = db.Column(db.String(256), nullable=True)
    phone_number = db.Column(db.String(256), nullable=False)
    position_type = db.Column(db.String(256), nullable=True)
    job_title = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return "<PersonModel: {} {}>".format(self.name, self.surname)

    def fullname(self):
        return "{} {}".format(self.name, self.username)


class EmailReceiverModel(db.Model, SaveMixin):
    id_email_received_model = db.Column(db.Integer, primary_key=True)
    email =  db.Column(db.String(256), nullable=False)
    subject =  db.Column(db.String(256), nullable=False)
    body =  db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<EmailReceiverModel: {} {}>".format(self.email, self.subject)