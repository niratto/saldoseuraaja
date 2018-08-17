from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from application.admin.forms import AdminForm
from application.auth.models import User
from datetime import datetime

@app.route("/admin", methods=["GET"])
@login_required
def admin_index():
    return render_template("admin/index.html", users = User.query.filter_by(admin=False))

@app.route("/admin/<user_id>/", methods=["POST"])
@login_required
def user_set_active_status(user_id):
    u = User.query.get(user_id)
    active = User.query.filter_by(id=user_id, active=True).first()

    if active:
        u.active = False
    else:
        u.active = True

    db.session().commit()

    return redirect(url_for("admin_index"))

@app.route("/admin/reset/<user_id>/", methods=["POST"])
@login_required
def user_reset_password(user_id):
    u = User.query.get(user_id)
    u.set_password(u.username[::-1])
    db.session().commit()

    flash("Käyttäjä: " + u.username)
    flash("Salasana on resetoitu (@ " + str(datetime.now()) + ")")
    flash("Salasana on nyt käyttäjätunnus väärinpäin!): " + u.username[::-1])
    return redirect(url_for("admin_index"))