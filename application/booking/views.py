from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from application.booking.forms import MoneysourceForm
from application.booking.models import Moneysource

@app.route("/booking", methods=["GET"])
@login_required
def booking_index():
    return render_template("booking/index.html")

@app.route("/source", methods=["GET","POST"])
@login_required
def moneysource():
    return render_template("booking/moneysource.html", sources = Moneysource.query.filter_by(acc_id_fk=current_user.id))

@app.route("/source/remove/<source_id>/", methods=["POST"])
@login_required
def remove_moneysource(source_id):
    ms = Moneysource.query.get(source_id)
    #msource = Moneysource.query.filter_by(acc_id_fk=user_id, ms_name=form.name.data).first()
    db.session().delete(ms)
    db.session().commit()

    flash("Rahalähde id:llä " + source_id + " on nyt poistettu")
    return redirect(url_for("moneysource"))

@app.route("/source/add/", methods = ["GET", "POST"])
@login_required
def add_moneysource():
    form = MoneysourceForm(request.form)
    
    if request.method == 'POST' and form.validate():
        m = Moneysource(form.name.data , form.info.data)
        m.acc_id_fk = current_user.id
        db.session().add(m)
        db.session.commit()
    
        return redirect(url_for('moneysource'))

    return render_template("booking/add_moneysource.html", form = form)
        
@app.route("/source/modify/<source_id>/", methods = ["POST","GET"])
@login_required
def modify_moneysource(source_id):
    # TODO: Tänne rahalähteen päivitys
    flash("HUOM! Muokkaa-ominaisuutta ei olla vielä toteutettu @ 17.8.2018")
    return redirect(url_for('moneysource'))