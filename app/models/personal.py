from app.extensions import db

class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String(255), nullable=True, default='0')
    mime_type = db.Column(db.String(255), nullable=True, default='0')
    gender = db.Column(db.String(10), nullable=True, default='0')
    dob = db.Column(db.Date, nullable=True)
    bio = db.Column(db.String(255), nullable=True, default='0')
    address = db.Column(db.String(255), nullable=True, default='0')
    address2 = db.Column(db.String(255), nullable=True, default='0')
    state = db.Column(db.String(100), nullable=True, default='0')
    city = db.Column(db.String(100), nullable=True, default='0')
    zipcode = db.Column(db.String(20), nullable=True, default='0')
    country = db.Column(db.String(100), nullable=True, default='0')
    address_type = db.Column(db.String(50), nullable=True, default='0')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('personals', lazy=True))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
