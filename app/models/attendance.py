from app.extensions import db
from datetime import datetime, time

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=True)
    attendance_year = db.Column(db.Integer, nullable=True) 
    attendance_month = db.Column(db.String(255), nullable=True)
    attendance_date = db.Column(db.Date, nullable=True)
    attendance_day = db.Column(db.String(255), nullable=True)
    attendance_status = db.Column(db.String(255), nullable=True, default='Present')
    holiday = db.Column(db.String(255), nullable=True, default='0')
    is_applied = db.Column(db.String(255), nullable=True, default='0')
    in_time = db.Column(db.Time, nullable=True, default=time(0, 0))
    out_time = db.Column(db.Time, nullable=True, default=time(0, 0))
    total_hours = db.Column(db.String(255), nullable=True, default='00:00')
    is_late = db.Column(db.Boolean, nullable=True, default=False)
    current_address = db.Column(db.String(255), nullable=True, default='0')
    coordinate = db.Column(db.String(255), nullable=True, default='0')
    comments = db.Column(db.String(255), nullable=True, default='NA')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # user = db.relationship('User', back_populates='attendances')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
