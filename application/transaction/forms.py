from flask_wtf import FlaskForm
from wtforms import DateField, BooleanField, StringField, DecimalField,validators
from wtforms.validators import Required, DataRequired
import datetime

class TransactionForm(FlaskForm):
    date = DateField('Päivämäärä', format = '%d.%m.%Y', default=datetime.date.today,validators=[DataRequired()])
    amount = DecimalField("Määrä (€)", [validators.DataRequired()])
    is_expense = BooleanField("Onko kyseessä tulo? (oletus: meno)")
    participant = StringField("Kohde:", [validators.DataRequired()])
    info = StringField("Lisätietoja:")

    class Meta:
        csrf = False
