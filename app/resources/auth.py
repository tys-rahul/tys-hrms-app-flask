from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re
from sqlalchemy.exc import IntegrityError

from app.utils.constants import (
    ERROR_MISSING_FIELDS,
    ERROR_INVALID_EMAIL,
    ERROR_INVALID_CONTACT,
    ERROR_USER_EXISTS_EMAIL,
    ERROR_USER_EXISTS_CONTACTNO,
    ERROR_USER_NOT_FOUND,
    ERROR_INVALID_CREDENTIALS,
    SUCCESS_USER_CREATED,
    SUCCESS_USER_UPDATED,
    SUCCESS_USER_DELETED,
)
auth_blueprint = Blueprint('auth', __name__)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_contact(contact):
    return len(contact) == 10 and contact.isdigit()

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    contact_no = data.get('contact_no')
    password = data.get('password')

    if not username or not password or not email or not contact_no:
        return jsonify({"response": ERROR_MISSING_FIELDS}), 400

    if not is_valid_email(email):
        return jsonify({"response": ERROR_INVALID_EMAIL}), 400

    if not is_valid_contact(contact_no):
        return jsonify({"response": ERROR_INVALID_CONTACT}), 400

    user_with_email = User.query.filter_by(email=email).first()
    user_with_contact_no = User.query.filter_by(contact_no=contact_no).first()
    if user_with_email:
        return jsonify({"response": ERROR_USER_EXISTS_EMAIL}), 409
    if user_with_contact_no:
        return jsonify({"response": ERROR_USER_EXISTS_CONTACTNO}), 409

    new_user = User(username=username, email=email, contact_no=contact_no)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"response": "An error occurred while creating the user"}), 500

    return jsonify({"response": SUCCESS_USER_CREATED}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"response": ERROR_MISSING_FIELDS}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"response": ERROR_INVALID_CREDENTIALS}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@auth_blueprint.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"response": ERROR_USER_NOT_FOUND}), 404
    return jsonify({"id": user.id, 'username': user.username, "email": user.email, "contact_no": user.contact_no}), 200

@auth_blueprint.route('/user/edit/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user(user_id):
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    contact_no = data.get('contact_no')

    if not username or not email or not contact_no:
        return jsonify({"response": ERROR_MISSING_FIELDS}), 400

    if not is_valid_email(email):
        return jsonify({"response": ERROR_INVALID_EMAIL}), 400

    if not is_valid_contact(contact_no):
        return jsonify({"response": ERROR_INVALID_CONTACT}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"response": ERROR_USER_NOT_FOUND}), 404

    # Check for unique constraints before updating
    existing_user_with_email = User.query.filter_by(email=email).first()
    existing_user_with_contact_no = User.query.filter_by(contact_no=contact_no).first()
    if existing_user_with_email and existing_user_with_email.id != user_id:
        return jsonify({"response": ERROR_USER_EXISTS_EMAIL}), 409
    if existing_user_with_contact_no and existing_user_with_contact_no.id != user_id:
        return jsonify({"response": ERROR_USER_EXISTS_CONTACTNO}), 409

    user.email = email
    user.username = username
    user.contact_no = contact_no

    db.session.commit()
    return jsonify({"response": SUCCESS_USER_UPDATED}), 200

@auth_blueprint.route('/user/reset-password', methods=['PUT'])
@jwt_required()
def update_password():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"response": "Email and new password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"response": "User with this email does not exist"}), 404

    # Updating the user's password
    user.set_password(password)
    db.session.commit()

    return jsonify({"response": "Password updated successfully"}), 200
