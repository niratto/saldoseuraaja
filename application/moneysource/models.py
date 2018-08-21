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