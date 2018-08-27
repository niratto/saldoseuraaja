from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for, session
from application.budget.models import Budget
from application.moneysource.models import Moneysource
from sqlalchemy.sql import text
from datetime import datetime, timedelta

@app.route("/reporting/<int:ms_id>", methods=["GET"])
@login_required
def reporting(ms_id):
    if ms_id == 0:
        sql = "select '(kaikki)' as ms_name,tr_month,sum(tr_amount) as tr_amount from transactions "
        sql += "inner join money_source on transactions.ms_id_fk=money_source.ms_id_pk "
        sql += "where transactions.acc_id_fk=" + str(current_user.id) + " "
        sql += "group by tr_month"
    else:
        sql = "select ms_name,tr_month,sum(tr_amount) as tr_amount from transactions "
        sql += "inner join money_source on transactions.ms_id_fk=money_source.ms_id_pk "
        sql += "where ms_id_pk=" + str(ms_id) + " and transactions.acc_id_fk=" + str(current_user.id) + " "
        sql += "group by ms_name, tr_month"

    print("******** SQL: " + sql + " **********")
    sum_transactions_per_month = db.engine.execute(text(sql))
    #q = db.session.query(Moneysource.ms_name,Transaction.tr_month,Transaction.tr_amount.join(Moneysource).filter(Transaction.acc_id_fk==current_user.id).filter(Transaction.ms_id_fk==Moneysource.ms_id_pk).order_by(Transaction.tr_month).asc()
    
    return render_template("reporting/reporting_index.html",sources = Moneysource.query.filter_by(acc_id_fk=current_user.id),data=sum_transactions_per_month)

@app.route("/reporting/saldo", methods=["GET"])
@login_required
def reporting_saldo():
    # jos kaveri alkaa manipuloimaan urlia ja poistaa raportin id:n, niin tehdään oletuskysely
    return render_template("reporting/reporting_saldo_index.html",budgets = Budget.query.filter_by(acc_id_fk=current_user.id))

@app.route("/reporting/saldo/<string:bu_id>", methods=["GET"])
@login_required
def reporting_saldo_budget(bu_id):
    # jos kaveri alkaa manipuloimaan urlia esim. string-muotoisilla syötteillä, niin tehdään oletusraportti
    # eli raportti jossa näkyy kaikki transaktiot per kuukausi
    
    budget_data = Budget.query.get(bu_id)
    #list = []
    bu_days = budget_data.bu_days_count + 1
    bu_amount = budget_data.bu_amount
    bu_daily_avg = budget_data.bu_avg_daily_consumption
    list = []

    saldo_amount_real_tmp = 0
    for day in range (0,bu_days):
        todellinen = True
        saldo_date = str(budget_data.bu_start_date + timedelta(days=day))
        
        saldo_amount_real = fetch_saldo_from_db(current_user.id, budget_data.ms_id_fk,saldo_date)
        if not saldo_amount_real:
            saldo_amount_real = saldo_amount_real_tmp - (saldo_amount_real_tmp / (bu_days - day))
            saldo_amount_real = float("{0:.2f}".format(saldo_amount_real))
            todellinen = False
        
        saldo_amount_calc = str(bu_amount - (bu_daily_avg * day))
        if todellinen:
            str_data = str(day) + "," + saldo_date + "," + str(saldo_amount_real) + "€," + saldo_amount_calc + "€"
        else:
            str_data = str(day) + "," + saldo_date + "," + str(saldo_amount_real) + "€*," + saldo_amount_calc + "€"
        
        list.append(str_data)
        saldo_amount_real_tmp = saldo_amount_real

    return render_template("reporting/reporting_saldo_index.html",budgets = Budget.query.filter_by(acc_id_fk=current_user.id), budget_data=list)

@app.route("/reporting/<string:ms_id>", methods=["GET"])
@login_required
def reporting_url_manipulation(ms_id):
    # jos kaveri alkaa manipuloimaan urlia esim. string-muotoisilla syötteillä, niin tehdään oletusraportti
    # eli raportti jossa näkyy kaikki transaktiot per kuukausi
    return default_query()

@app.route("/reporting", methods=["GET"])
@login_required
def reporting_url_manipulation2():
    # jos kaveri alkaa manipuloimaan urlia ja poistaa raportin id:n, niin tehdään oletuskysely
    return default_query()

@app.route("/reporting/", methods=["GET"])
@login_required
def reporting_url_manipulation3():
    # jos kaveri alkaa manipuloimaan urlia ja poistaa raportin id:n, niin tehdään oletuskysely
    return default_query()

def default_query():
    sql = "select '(kaikki)' as ms_name,tr_month,sum(tr_amount) as tr_amount from transactions "
    sql += "inner join money_source on transactions.ms_id_fk=money_source.ms_id_pk "
    sql += "where transactions.acc_id_fk=" + str(current_user.id) + " "
    sql += "group by tr_month"

    sum_transactions_per_month = db.engine.execute(text(sql))

    return render_template("reporting/reporting_index.html",sources = Moneysource.query.filter_by(acc_id_fk=current_user.id),data=sum_transactions_per_month)

def default_saldo_query():
    sql = "select '(kaikki)' as ms_name,tr_month,sum(tr_amount) as tr_amount from transactions "
    sql += "inner join money_source on transactions.ms_id_fk=money_source.ms_id_pk "
    sql += "where transactions.acc_id_fk=" + str(current_user.id) + " "
    sql += "group by tr_month"

    sum_transactions_per_month = db.engine.execute(text(sql))

    return render_template("reporting/reporting_index.html",sources = Moneysource.query.filter_by(acc_id_fk=current_user.id),data=sum_transactions_per_month)

def fetch_saldo_from_db(acc_id,ms_id,date):
    sql = "select sa_amount from saldo where sa_date ='" + str(date) + "' and ms_id_fk = " + str(ms_id) + " and acc_id_fk = " + str(acc_id)
    
    ret = db.engine.execute(text(sql)).first()
    
    if ret:
        return ret[0]
    else:
        return 0