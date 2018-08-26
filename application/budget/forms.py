from flask_wtf import FlaskForm
from wtforms import DateField, StringField, validators, DecimalField
from wtforms.validators import DataRequired
import datetime

class BudgetForm(FlaskForm):
    bname = StringField("Budjetin nimi", [validators.DataRequired()])
    bamount = DecimalField("Määrä (€)", [validators.DataRequired()])  
    bstart_date = DateField('Alotuspäivämäärä', format = '%d.%m.%Y', default=datetime.date.today,validators=[DataRequired()])
    bend_date = DateField('Lopetusäivämäärä', format = '%d.%m.%Y',validators=[DataRequired()])
    
    class Meta:
        csrf = False
