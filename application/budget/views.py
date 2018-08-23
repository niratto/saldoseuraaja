from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from application.saldo.forms import SaldoForm
from application.budget.models import Budget
from application.moneysource.models import Moneysource

@app.route("/budget", methods=["GET","POST"])
@login_required
def budget():
    q = db.session.query(Budget.bu_id_pk,Budget.bu_name,Budget.bu_amount,Budget.bu_start_date,Budget.bu_end_date,Moneysource.ms_name).join(Moneysource).filter(Budget.acc_id_fk==current_user.id).filter(Budget.ms_id_fk==Moneysource.ms_id_pk).order_by(Budget.ms_id_fk,Budget.bu_name.desc())
    return render_template("budget/budget.html", budgets = q)

@app.route("/budget/add/", methods = ["GET", "POST"])
@login_required
def add_budget():
    #form = SaldoForm(request.form)
    #
    #if request.method == 'POST' and form.validate():
    #    s = Saldo(form.date.data, form.amount.data)
    #    s.acc_id_fk = current_user.id
    #    s.ms_id_fk = request.form.get('msource_dropdown')
    #    db.session().add(s)
    #    db.session.commit()

        return redirect(url_for('saldo'))
    #elif request.method == 'POST' and not form.validate():
    #    sources = Moneysource.query.filter_by(acc_id_fk=current_user.id)
    #    return render_template('saldo/add_saldo.html', form = form, sources=sources)
    #else:
    #    sources = Moneysource.query.filter_by(acc_id_fk=current_user.id)
    #    return render_template('saldo/add_saldo.html', form = form, sources=sources)

@app.route("/budget/remove/<int:sa_id>/", methods=["POST"])
@login_required
def remove_budget(bu_id):
    b = Saldo.query.get(bu_id)
    #msource = Moneysource.query.filter_by(acc_id_fk=user_id, ms_name=form.name.data).first()
    db.session().delete(b)
    db.session().commit()

    flash("poistettu")
    return redirect(url_for("budget"))

@app.route("/budget/modify/<int:bu_id>", methods = ["GET","POST"])
@login_required
def modify_budget(bu_id):
    
    #s = Saldo.query.get(sa_id)
    #
    #if s:
    #    form = SaldoForm(formdata=request.form)
    #    if request.method == 'POST' and form.validate():
    #        s.sa_date = form.date.data
    #        s.sa_amount = form.amount.data
    #        s.acc_id_fk = current_user.id
    #        s.ms_id_fk = request.form.get('msource_dropdown')
    #        db.session.commit()
            return redirect(url_for('saldo'))
    #    else:
    #        form.date.data = s.sa_date
    #        form.amount.data = s.sa_amount
    #        current_msource = s.ms_id_fk
    #        sources = Moneysource.query.filter_by(acc_id_fk=current_user.id)
    #        return render_template('saldo/modify_saldo.html', form=form, sa_id=sa_id, ms_id=current_msource, sources=sources)
    #else:
    #   return 'Error loading #{id}'.format(id=id)

