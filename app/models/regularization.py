from datetime import datetime, timezone
from app.extensions import db

class Regularization(db.Model):
    __tablename__ = 'regularizations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    att_id = db.Column(db.Integer, db.ForeignKey('attendance.id'), nullable=True)  # Use only this column for Attendance foreign key
    email = db.Column(db.String(255), nullable=True)
    att_date = db.Column(db.Date, nullable=True)
    reason = db.Column(db.String(255), nullable=True)
    comment = db.Column(db.String(255), nullable=True, default='NA')
    status = db.Column(db.String(50), nullable=True, default='Pending', comment='Pending/Approved/Rejected')
    label = db.Column(db.String(50), nullable=True, default='RG')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    attendance = db.relationship('Attendance', back_populates='regularizations', foreign_keys=[att_id])
    user = db.relationship('User', back_populates='regularizations')
    
