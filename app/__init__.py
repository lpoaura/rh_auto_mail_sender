from flask import Flask
from app.routes import main_bp

app = Flask(__name__)

app.register_blueprint(main_bp, url_prefix="/")