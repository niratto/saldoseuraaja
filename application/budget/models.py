from application import db
import datetime

class Budget(db.Model):
    __tablename__ = "budget"

    bu_id_pk = db.Column(db.Integer, primary_key=True)
    bu_name = db.Column(db.String(255), nullable=False)
    bu_amount = db.Column(db.Numeric(10,2), nullable=False)
    bu_start_date = db.Column(db.Date, nullable=False)
    bu_end_date = db.Column(db.Date, nullable=False)
    bu_days_count = db.Column(db.Integer, nullable=False)
    bu_avg_daily_consumption = db.Column(db.Numeric(10,2), nullable=False)

    # sa_id_fk = db.Column(db.Integer, db.ForeignKey('saldo.sa_id_pk'),
    #                       nullable=False)
    ms_id_fk = db.Column(db.Integer, db.ForeignKey('money_source.ms_id_pk'),
                           nullable=False)
    acc_id_fk = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

    def __init__(self, name, amount, start_date, end_date):
        self.bu_name = name
        self.bu_amount = amount
        self.bu_start_date = start_date
        self.bu_end_date = end_date
        self.bu_days_count = self.pv_lkm(start_date, end_date)
        self.bu_avg_daily_consumption = self.bu_amount / self.bu_days_count
        self.done = False

    def pv_lkm(self, before, after):
        d1 = before
        d2 = after
        return abs(d1 - d2).days