from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from application.saldo.forms import SaldoForm
from application.saldo.models import Saldo
from application.moneysource.models import Moneysource

@app.route("/saldo", methods=["GET","POST"])
@login_required
def saldo():
    q = db.session.query(Saldo.sa_date,Saldo.sa_amount,Moneysource.ms_name).join(Moneysource).filter(Saldo.acc_id_fk==current_user.id).filter(Saldo.ms_id_fk==Moneysource.ms_id_pk).all() 
    return render_template("saldo/saldo.html", sources = q)

@app.route("/saldo/add/", methods = ["GET", "POST"])
@login_required
def add_saldo():
    form = SaldoForm(request.form)
    
    if request.method == 'POST' and form.validate():
        s = Saldo(form.date.data, form.amount.data)
        s.acc_id_fk = current_user.id
        s.ms_id_fk = request.form.get('msource_dropdown')
        db.session().add(s)
        db.session.commit()

        return redirect(url_for('saldo'))
    elif request.method == 'POST' and not form.validate():
        sources = Moneysource.query.filter_by(acc_id_fk=current_user.id)
        return render_template('saldo/add_saldo.html', form = form, sources=sources)
    else:
        sources = Moneysource.query.filter_by(acc_id_fk=current_user.id)
        return render_template('saldo/add_saldo.html', form = form, sources=sources)

@app.route("/saldo/remove/<int:sa_id>/", methods=["POST"])
@login_required
def remove_saldo(sa_id):
    t = Transaction.query.get(tr_id)
    #msource = Moneysource.query.filter_by(acc_id_fk=user_id, ms_name=form.name.data).first()
    #db.session().delete(t)
    #db.session().commit()

    flash("poistettu")
    return redirect(url_for("booking_index"))

@app.route("/saldo/modify/<int:sa_id>", methods = ["GET","POST"])
@login_required
def modify_saldo(sa_id):
    
    s = Saldo.query.get(sa_id)
    
    if s:
        form = SaldoForm(formdata=request.form)
        if request.method == 'POST' and form.validate():
            return redirect(url_for('booking_index'))
        else:
            return render_template('saldo/modify_saldo.html', form=form, sa_id=sa_id)
    else:
        return 'Error loading #{id}'.format(id=id)
