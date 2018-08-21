from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from application.transaction.models import Transaction

@app.route("/booking", methods=["GET"])
@login_required
def booking_index():
    return render_template("booking/index.html", transactions = Transaction.query.filter_by(acc_id_fk=current_user.id).order_by(Transaction.tr_date.desc()))
