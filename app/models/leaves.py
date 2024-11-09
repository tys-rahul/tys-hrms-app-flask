from datetime import datetime, timezone
from app.extensions import db

class Leave(db.Model):
    __tablename__ = 'leaves'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=True, default=None)
    end_date = db.Column(db.Date, nullable=True, default=None)
    reason = db.Column(db.String(255), nullable=True, default='NA')
    comment = db.Column(db.String(255), nullable=True, default='NA')
    status = db.Column(db.String(50), nullable=True, default='Pending', comment='Pending/Approved/Rejected')
    applied_on = db.Column(db.Date, nullable=True, default=lambda: datetime.now(timezone.utc).date())
    label = db.Column(db.String(50), nullable=True, default='LV')
    leave_type = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref='leaves')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.leave_type = "AL" if not self.end_date else "FL"
