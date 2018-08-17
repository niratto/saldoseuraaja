from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators

class MoneysourceForm(FlaskForm):
    name = StringField("Rahalähteen nimi:", [validators.DataRequired()])
    info = StringField("Lisätietoja:")

    class Meta:
        csrf = False
