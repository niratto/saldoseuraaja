from application import app, db
from flask_login import login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for, session
from application.transaction.models import Transaction
from application.moneysource.models import Moneysource
from sqlalchemy.sql import text

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
        sql += "group by tr_month"

    print("******** SQL: " + sql + " **********")
    sum_transactions_per_month = db.engine.execute(text(sql))
    #q = db.session.query(Moneysource.ms_name,Transaction.tr_month,Transaction.tr_amount.join(Moneysource).filter(Transaction.acc_id_fk==current_user.id).filter(Transaction.ms_id_fk==Moneysource.ms_id_pk).order_by(Transaction.tr_month).asc()
    
    return render_template("reporting/reporting_index.html",sources = Moneysource.query.filter_by(acc_id_fk=current_user.id),data=sum_transactions_per_month)

@app.route("/reporting/saldo", methods=["GET"])
@login_required
def reporting_saldo():
    # jos kaveri alkaa manipuloimaan urlia ja poistaa raportin id:n, niin tehdään oletuskysely
    return render_template("reporting/reporting_saldo_index.html")

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
