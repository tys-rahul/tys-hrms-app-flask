from app.extensions import db

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university_name = db.Column(db.String(255), nullable=False)
    course_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.String(80), nullable=False)
    end_date = db.Column(db.String(80), nullable=False)
    grade = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('educations', lazy=True))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
