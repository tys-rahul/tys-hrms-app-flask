from app.extensions import db

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(255), nullable=True, default='0')
    account_no = db.Column(db.String(255), nullable=True, default='0')
    ifsc_code = db.Column(db.String(255), nullable=True, default='0')
    branch_name = db.Column(db.String(255), nullable=True, default='0')
    bank_address = db.Column(db.String(255), nullable=True, default='0')
    pan_card = db.Column(db.String(255), nullable=True, default='0')
    aadhar_card = db.Column(db.String(255), nullable=True, default='0')
    aadhar_img = db.Column(db.String(255), nullable=True)
    pan_img = db.Column(db.String(255), nullable=True)
    bank_passbook_img = db.Column(db.String(255), nullable=True)
    label = db.Column(db.String(255), nullable=True, default='BK')
    status = db.Column(db.String(10), nullable=True, comment='0: Approved, 1: Pending, 2: Rejected')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
