from application import app, db
from flask import redirect, render_template, request, url_for
from application.register.forms import RegistrationForm
from application.auth.models import User
from application.booking.models import Moneysource

@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    adminExists = User.query.filter_by(admin=True).first()

    if request.method == 'POST' and form.validate():
        #user = User(form.username.data, form.password.data)
        user = User.query.filter_by(username=form.username.data).first()
        
        if user:
            return render_template("register/register.html", form = form,
                               error = "Antamasi käyttäjätunnus löytyy jo tietokannasta!")

        if not adminExists:
            u = User(form.name.data , form.username.data, form.password2.data)
            u.active = True
            u.admin = True
        else:
            u = User(form.name.data , form.username.data, form.password2.data)
            u.active = True
            u.admin = False

        db.session().add(u)
        db.session.commit()
        return redirect(url_for('auth_login'))
    elif not adminExists:
        return render_template('register/register_admin.html', form=form)
    else:
        return render_template('register/register.html', form=form)


    return render_template('register/register.html', form=form)