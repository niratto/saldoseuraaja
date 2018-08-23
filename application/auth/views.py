from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db
from application.moneysource.models import Moneysource
from application.auth.models import User
from application.auth.forms import LoginForm


@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    
    # katsotaan löytyykö kirjautuva käyttäjätunnus tietokannasta
    user = User.query.filter_by(username=form.username.data).first()
    active_user = User.query.filter_by(username=form.username.data,active=True).first()
    # katsotaan, täsmääkö käyttäjän suolatu salasana vs. selkokielisenä annettu salasana
    
    try:
        pwd_ok = user.check_password(form.password.data)
    except AttributeError:
        return render_template("auth/loginform.html", form = form,
                               error = "Antamasi tunnus tai salasana ei kelpaa!")
    
    # jos käyttäjää ei löydy tai salasana ei täsmää, niin ilmoitetaan herja käyttäjälle
    if not user or not pwd_ok:
        return render_template("auth/loginform.html", form = form,
                               error = "Antamasi tunnus tai salasana ei kelpaa!")
    elif not active_user:
        return render_template("auth/loginform.html", form = form,
                               error = "Ylläpitäjä on deaktivoinut käyttäjätunnuksesi!")

    login_user(user)

    # katsotaan onko käyttäjä admin vai ei
    adminExists = User.query.filter_by(username=form.username.data, admin=True).first()

    if adminExists:
        return redirect(url_for("admin_index"))
    else:
        # katsotaan onko käyttäjän money_source -taulussa mitään merkintää kirjautumisen ohessa
        # jos merkintöjä ei vielä ole, niin luodaan kirjautumisen ohessa yksi merkintä, jolle 
        # annetaan arvoksi (ms_name): Käteinen
        # Ideana tässä on se, että kaikilla on joskus käteistä :) ja siksi käyttäjällä on hyvä
        # olla heti luomisvaiheessa yksi rahanlähde ja olkoon se tässä käteinen.
        # Käyttäjä voi sitten myöhemmässä vaiheessa lisäillä lisää rahalähteitään...
        m = Moneysource("Käteinen","")
        m.acc_id_fk = current_user.id
        
        exists = Moneysource.query.filter_by(acc_id_fk=current_user.id).first()
        
        if not exists:
            db.session().add(m)
            db.session.commit()
            
        return redirect(url_for("booking_index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("auth_login")) 
