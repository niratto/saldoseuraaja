from flask_wtf import FlaskForm
from wtforms import DateField, StringField, DecimalField,validators
from wtforms.validators import Required, DataRequired
import datetime

class SaldoForm(FlaskForm):
    date = DateField('Päivämäärä', format = '%d.%m.%Y', default=datetime.date.today,validators=[DataRequired()])
    amount = DecimalField("Määrä (€)", [validators.DataRequired()])
    

    class Meta:
        csrf = False
