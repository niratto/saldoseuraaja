from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
  
class RegistrationForm(FlaskForm):
    name = StringField("Nimi/lempinimi/alias/...", [validators.DataRequired()])
    username = StringField("Käyttäjätunnus" ,[validators.DataRequired()])
    password = PasswordField('Anna salasana', [
        validators.DataRequired(),
        validators.EqualTo('password2', message=('Salasanana vahvistus ei onnistunut'))
    ])
    password2 = PasswordField("Vahvista salasana")


    class Meta:
        csrf = False