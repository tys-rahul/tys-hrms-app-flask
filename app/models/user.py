from werkzeug.security import generate_password_hash, check_password_hash
from app.models.role import Role
from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    contact_no = db.Column(db.String(10), unique=True, nullable=False)
    status = db.Column(db.String(1), default='0', comment="0 for active, 1 for inactive")
    work_location_type = db.Column(db.String(1), default='0', comment="0 for Office, 1 for Remote")
    user_type = db.Column(db.String(1), default='0', comment="0 for probation, 1 for permanent")
    roles = db.relationship('Role', secondary='user_roles', backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Use back_populates to link with the ExperienceDetails model's 'user' attribute
    experiences = db.relationship('ExperienceDetails', back_populates='user', lazy=True)
    regularizations = db.relationship('Regularization', back_populates='user')


