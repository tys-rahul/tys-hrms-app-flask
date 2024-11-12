from app.extensions import db
from datetime import date

class Reimbursement(db.Model):
    __tablename__ = 'reimbursements'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    upi_id = db.Column(db.String, nullable=True)
    expense_date = db.Column(db.Date, nullable=False)
    expense_item = db.Column(db.String, nullable=False)
    expense_cost = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    sum = db.Column(db.String, nullable=False)
    receipt = db.Column(db.String, default='NA')
    total_amt = db.Column(db.String, nullable=False)
    ref_no = db.Column(db.String, nullable=True, default='NA', comment='payment reference')
    status = db.Column(db.String, default='Pending')
    label = db.Column(db.String, default='RM')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


