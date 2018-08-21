from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from application.transaction.forms import TransactionForm
from application.transaction.models import Transaction

@app.route("/transaction/add/", methods = ["GET", "POST"])
@login_required
def add_transaction():
    form = TransactionForm(request.form)
    fixed_amount = 0

    if request.method == 'POST' and form.validate():
        if form.is_expense.data == False:
            fixed_amount = form.amount.data * -1
        else:
            fixed_amount = form.amount.data

        t = Transaction(form.date.data , fixed_amount, form.participant.data, form.info.data)
        t.acc_id_fk = current_user.id
        db.session().add(t)
        db.session.commit()

        return redirect(url_for('booking_index'))
    elif request.method == 'POST' and not form.validate():
        return render_template('transaction/add_transaction.html', form = form)
    else:
        return render_template('transaction/add_transaction.html', form = form)

@app.route("/transaction/remove/<int:tr_id>/", methods=["POST"])
@login_required
def remove_transaction(tr_id):
    t = Transaction.query.get(tr_id)
    #msource = Moneysource.query.filter_by(acc_id_fk=user_id, ms_name=form.name.data).first()
    db.session().delete(t)
    db.session().commit()

    flash("poistettu")
    return redirect(url_for("booking_index"))

@app.route("/transaction/modify/<int:tr_id>", methods = ["GET","POST"])
@login_required
def modify_transaction(tr_id):
    
    t = Transaction.query.get(tr_id)
    
    if t:
        form = TransactionForm(formdata=request.form)
        if request.method == 'POST' and form.validate():
            t.tr_id_pk = tr_id
            t.tr_date = form.date.data

            if form.is_expense.data == False and form.amount.data > 0:
                fixed_amount = form.amount.data * -1
            elif form.is_expense.data == True and form.amount.data < 0:
                fixed_amount = form.amount.data * -1
            else:
                fixed_amount = form.amount.data

            t.tr_amount = fixed_amount
            t.tr_participant = form.participant.data
            t.tr_info = form.info.data
            t.acc_id_fk = current_user.id
            
            db.session.commit()
            # save edits
            #save_changes(album, form)
            return redirect(url_for('booking_index'))
        else:
            form.date.data = t.tr_date
            form.amount.data = t.tr_amount
            form.participant.data = t.tr_participant

            if t.tr_amount > 0:
                form.is_expense.data = True
            else:
                form.is_expense.data = False

            form.info.data = t.tr_info
            return render_template('transaction/modify_transaction.html', form=form, tr_id=tr_id)
    else:
        return 'Error loading #{id}'.format(id=id)
