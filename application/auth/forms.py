from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus", [validators.DataRequired()])
    password = PasswordField("Salasana", [validators.DataRequired()])
  
    class Meta:
        csrf = False
