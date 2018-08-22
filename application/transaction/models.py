from application import db

class Transaction(db.Model):
    __tablename__ = "transactions"

    tr_id_pk = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    tr_date = db.Column(db.Date, nullable=False)
    tr_amount = db.Column(db.Numeric(10,2), nullable=False)
    tr_participant = db.Column(db.String(255))
    tr_info = db.Column(db.String(255))
    
    ms_id_fk = db.Column(db.Integer, db.ForeignKey('money_source.ms_id_pk'),
                           nullable=False)
    acc_id_fk = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

    def __init__(self, date, amount, participant,info):
        self.tr_date = date
        self.tr_amount = amount
        self.tr_participant = participant
        self.tr_info = info
        self.done = False