from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from application.saldo.forms import SaldoForm
from application.saldo.models import Saldo
from application.moneysource.models import Moneysource
from sqlalchemy.sql import text

@app.route("/saldo", methods=["GET","POST"])
@login_required
def saldo():
    sql = "select max(sa_date) as sa_date,sa_amount,ms_name "
    sql += "from saldo "
    sql += "inner join money_source on saldo.ms_id_fk = money_source.ms_id_pk "
    sql += "where saldo.acc_id_fk = " + str(current_user.id) + " "
    sql += "group by ms_name order by sa_amount desc"

    print("******** SQL: " + sql + " **********")
    saldo_latest = db.engine.execute(text(sql))
    saldo_all = db.session.query(Saldo.sa_id_pk,Saldo.sa_date,Saldo.sa_amount,Moneysource.ms_name).join(Moneysource).filter(Saldo.acc_id_fk==current_user.id).filter(Saldo.ms_id_fk==Moneysource.ms_id_pk).order_by(Saldo.sa_date.desc())
    return render_template("saldo/saldo.html", saldos_latest = saldo_latest, saldos_all = saldo_all)

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
    s = Saldo.query.get(sa_id)
    #msource = Moneysource.query.filter_by(acc_id_fk=user_id, ms_name=form.name.data).first()
    db.session().delete(s)
    db.session().commit()

    flash("poistettu")
    return redirect(url_for("saldo"))

@app.route("/saldo/modify/<int:sa_id>", methods = ["GET","POST"])
@login_required
def modify_saldo(sa_id):
    
    s = Saldo.query.get(sa_id)
    
    if s:
        form = SaldoForm(formdata=request.form)
        if request.method == 'POST' and form.validate():
            s.sa_date = form.date.data
            s.sa_amount = form.amount.data
            s.acc_id_fk = current_user.id
            s.ms_id_fk = request.form.get('msource_dropdown')
            db.session.commit()
            return redirect(url_for('saldo'))
        else:
            form.date.data = s.sa_date
            form.amount.data = s.sa_amount
            current_msource = s.ms_id_fk
            sources = Moneysource.query.filter_by(acc_id_fk=current_user.id)
            return render_template('saldo/modify_saldo.html', form=form, sa_id=sa_id, ms_id=current_msource, sources=sources)
    else:
        return 'Error loading #{id}'.format(id=id)

