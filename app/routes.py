from flask import Blueprint
from flask import render_template

main_bp = Blueprint('mail', __name__, template_folder='templates')

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/hello')
def hello():
    return 'Hello, World'