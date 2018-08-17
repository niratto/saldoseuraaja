from application import db

class Moneysource(db.Model):
    __tablename__ = "money_source"

    ms_id_pk = db.Column(db.Integer, primary_key=True)
    ms_name = db.Column(db.String(255), nullable=False)
    ms_extrainfo = db.Column(db.String(255), nullable=True)

    acc_id_fk = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

    def __init__(self, name, info):
        self.ms_name = name
        self.ms_extrainfo = info
        self.done = False

class Transactions(db.Model):
    __tablename__ = "transactions"

    tr_id_pk = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    tr_date = db.Column(db.DateTime, nullable=False)
    tr_amount = db.Column(db.Numeric(10,2), nullable=False)
    tr_expense = db.Column(db.Boolean, default=True)
    tr_participant = db.Column(db.String(255))
    tr_info = db.Column(db.String(255))
    
    acc_id_fk = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

    def __init__(self, name, info):
        self.ms_name = name
        self.ms_extrainfo = info
        self.done = False