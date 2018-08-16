from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm
from application.booking.models import Moneysource

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "Antamasi tunnus tai salasana ei kelpaa!")


    login_user(user)

    m = Moneysource("Käteinen","")
    m.acc_id_fk = current_user.id
    
    exists = Moneysource.query.filter_by(acc_id_fk=current_user.id).first()
    
    # katsotaan onko käyttäjän money_source -taulussa mitään merkintää kirjautumisen ohessa
    # jos merkintöjä ei vielä ole, niin luodaan kirjautumisen ohessa yksi merkintä, jolle 
    # annetaan arvoksi (ms_name): Käteinen
    # Ideana tässä on se, että kaikilla on joskus käteistä :) ja siksi käyttäjällä on hyvä
    # olla heti luomisvaiheessa yksi rahanlähde ja olkoon se tässä käteinen.
    # Käyttäjä voi sitten myöhemmässä vaiheessa lisäillä lisää rahalähteitään...
    if not exists:
        db.session().add(m)
        db.session.commit()
        
    return redirect(url_for("booking_index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("auth_login")) 
