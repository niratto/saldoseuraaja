from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from application.budget.forms import BudgetForm
from application.budget.models import Budget
from application.moneysource.models import Moneysource
from datetime import datetime

@app.route("/budget", methods=["GET","POST"])
@login_required
def budget():
    q = db.session.query(Budget.bu_id_pk,Budget.bu_name,Budget.bu_amount,Budget.bu_start_date,Budget.bu_end_date,Budget.bu_days_count,Budget.bu_avg_daily_consumption,Moneysource.ms_name).join(Moneysource).filter(Budget.acc_id_fk==current_user.id).filter(Budget.ms_id_fk==Moneysource.ms_id_pk).order_by(Budget.ms_id_fk,Budget.bu_name.desc())
    return render_template("budget/budget.html", budgets = q)

@app.route("/budget/add/", methods = ["GET", "POST"])
@login_required
def add_budget():
    form = BudgetForm(request.form)
    
    if request.method == 'POST' and form.validate():
        b = Budget(form.bname.data, form.bamount.data, form.bstart_date.data, form.bend_date.data)
        b.acc_id_fk = current_user.id
        b.ms_id_fk = request.form.get('msource_dropdown')
        db.session().add(b)
        db.session.commit()

        return redirect(url_for('budget'))
    elif request.method == 'POST' and not form.validate():
        sources = Moneysource.query.filter_by(acc_id_fk=current_user.id)
        return render_template('budget/add_budget.html', form = form, sources=sources)
    else:
        sources = Moneysource.query.filter_by(acc_id_fk=current_user.id)
        return render_template('budget/add_budget.html', form = form, sources=sources)

@app.route("/budget/remove/<int:bu_id>/", methods=["POST"])
@login_required
def remove_budget(bu_id):
    b = Budget.query.get(bu_id)
    #msource = Moneysource.query.filter_by(acc_id_fk=user_id, ms_name=form.name.data).first()
    db.session().delete(b)
    db.session().commit()

    flash("poistettu")
    return redirect(url_for("budget"))

@app.route("/budget/modify/<int:bu_id>", methods = ["GET","POST"])
@login_required
def modify_budget(bu_id):
    form = BudgetForm(request.form)
    b = Budget.query.get(bu_id)
    
    if b:
        if request.method == 'POST' and form.validate():
            start_date = form.bstart_date.data
            end_date = form.bend_date.data

            print("****** OK ***********")
            b.bu_name = form.bname.data
            b.bu_amount = form.bamount.data
            b.bu_start_date = form.bstart_date.data
            b.bu_end_date = form.bend_date.data
            b.bu_days_count = (end_date - start_date).days
            b.bu_avg_daily_consumption = b.bu_amount / b.bu_days_count
            b.acc_id_fk = current_user.id
            b.ms_id_fk = request.form.get('msource_dropdown')

            db.session.commit()
            return redirect(url_for('budget'))
        else:            
            print("****** NOT OK ***********")
            form.bname.data = b.bu_name 
            form.bamount.data = b.bu_amount
            form.bstart_date.data = b.bu_start_date
            form.bend_date.data = b.bu_end_date
            current_msource = b.ms_id_fk
            sources = Moneysource.query.filter_by(acc_id_fk=current_user.id)
            return render_template('budget/modify_budget.html', form=form, bu_id=bu_id, ms_id=current_msource, sources=sources)
    else:
       return 'Error loading #{id}'.format(id=id)

