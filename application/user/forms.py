from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators

class UserEditForm(FlaskForm):
    name = StringField("Nimi/lempinimi/alias/...")
    password = PasswordField('Anna uusi salasana', [
        validators.EqualTo('password2', message=('Salasanana vahvistus ei onnistunut'))
    ])
    password2 = PasswordField("Vahvista uusi salasana")

    class Meta:
        csrf = False