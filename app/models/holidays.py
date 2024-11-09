from datetime import datetime, timezone
from app.extensions import db

class Holidays(db.Model):
    __tablename__ = 'holidays'

    id = db.Column(db.Integer, primary_key=True)
    holiday_date = db.Column(db.Date, nullable=True)
    holiday_name = db.Column(db.String(255), nullable=True, default='NA')
    month = db.Column(db.String(20), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
