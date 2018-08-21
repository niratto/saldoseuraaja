from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from application.transaction.forms import TransactionForm
from application.transaction.models import Transaction

@app.route("/transaction/add/", methods = ["GET", "POST"])
@login_required
def add_transaction():
    form = TransactionForm(request.form)
    
    if request.method == 'POST' and form.validate():
        #m = Moneysource(form.name.data , form.info.data)
        #m.acc_id_fk = current_user.id
        #db.session().add(m)
        #db.session.commit()
    
        return redirect(url_for('booking'))

    return render_template('transaction/add_transaction.html', form = form)