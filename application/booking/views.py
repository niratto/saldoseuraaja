from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for, session
from application.transaction.models import Transaction
from application.moneysource.models import Moneysource

@app.route("/booking", methods=["GET"])
@login_required
def booking_index():
    q = db.session.query(Transaction.tr_id_pk,Transaction.tr_date,Transaction.tr_amount,Moneysource.ms_name,Transaction.tr_participant,Transaction.tr_info).join(Moneysource).filter(Transaction.acc_id_fk==current_user.id).filter(Transaction.ms_id_fk==Moneysource.ms_id_pk).order_by(Transaction.tr_date.desc())
    #order_by(Transaction.tr_date.desc())
    
    return render_template("booking/index.html", transactions = q)

    
