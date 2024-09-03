from app.extensions import db

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(80), nullable=False)
    prev_experience = db.Column(db.String(80), default='0')
    experience = db.Column(db.String(80), default='0')
    salary = db.Column(db.BigInteger, nullable=True, default=0)
    skills = db.Column(db.String(255), nullable=True, default='NA')
    cv_intro = db.Column(db.String(255), nullable=True, default='NA')
    joining_date = db.Column(db.String(80), nullable=True, default='0')
    permanent_confirm_date = db.Column(db.String(80), nullable=True, default='NA')
    termination_date = db.Column(db.String(80), nullable=True, default='00:00:0000')
    termination_reason = db.Column(db.String(255), nullable=True, default='0')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('professionals', lazy=True))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
