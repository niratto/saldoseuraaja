from application import db

class Saldo(db.Model):
    __tablename__ = "saldo"
    sa_id_pk = db.Column(db.Integer, primary_key=True)
    sa_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    sa_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    sa_date = db.Column(db.Date, nullable=False)
    sa_amount = db.Column(db.Numeric(10,2), nullable=False)

    ms_id_fk = db.Column(db.Integer,db.ForeignKey('money_source.ms_id_pk'))
    acc_id_fk = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

    def __init__(self, date, amount):
        self.sa_date = date
        self.sa_amount = amount
        