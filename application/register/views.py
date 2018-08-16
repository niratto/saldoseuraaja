from application import app, db
from flask import redirect, render_template, request, url_for
from application.register.forms import RegistrationForm
from application.auth.models import User
from application.booking.models import Moneysource

@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #user = User(form.username.data, form.password.data)
        user = User.query.filter_by(username=form.username.data).first()
        
        if user:
            return render_template("register/register.html", form = form,
                               error = "Antamasi käyttäjätunnus löytyy jo tietokannasta!")
        
        u = User(form.name.data , form.username.data, form.password2.data)
        
        db.session().add(u)
        db.session.commit()
        return redirect(url_for('auth_login'))
    else:
        return render_template('register/register.html', form=form)


    return render_template('register/register.html', form=form)