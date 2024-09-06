from app.extensions import db

class OfficeLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    office_location = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True, default=0)
    longitude = db.Column(db.Float, nullable=True, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

def __init__(self, **kwargs):
        super().__init__(**kwargs)
