from flask import Flask
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()

app = Flask(__name__)
app.config.from_pyfile('config.py')
csrf.init_app(app)

from app import views, models, forms
