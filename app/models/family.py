from app.extensions import db
from datetime import datetime

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    father_name = db.Column(db.String(100), nullable=True, default="")
    mother_name = db.Column(db.String(100), nullable=True, default="")
    personal_email = db.Column(db.String(100), nullable=True, default="")
    alternate_contact = db.Column(db.String(100), nullable=True, default="")
    family_address = db.Column(db.String(255), nullable=True, default="")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('families', lazy=True))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)