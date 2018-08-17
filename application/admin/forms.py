from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators

class AdminForm(FlaskForm):

    class Meta:
        csrf = False