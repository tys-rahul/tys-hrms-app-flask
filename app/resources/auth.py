from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.role import  Role, UserRoles
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
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': ERROR_MISSING_FIELDS
            }), 400

    if not is_valid_email(email):
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': ERROR_INVALID_EMAIL
            }), 400

    if not is_valid_contact(contact_no):
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': ERROR_INVALID_CONTACT
            }), 400

    user_with_email = User.query.filter_by(email=email).first()
    user_with_contact_no = User.query.filter_by(contact_no=contact_no).first()
    if user_with_email:
        return jsonify({
                'success': False,
                'status_code': 409,
                'data': [],
                'message': ERROR_USER_EXISTS_EMAIL
            }), 409
    if user_with_contact_no:
        return jsonify({
                'success': False,
                'status_code': 409,
                'data': [],
                'message': ERROR_USER_EXISTS_CONTACTNO
            }), 409

    new_user = User(username=username, email=email, contact_no=contact_no)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
                'success': False,
                'status_code': 500,
                'data': [],
                'message': "An error occurred while creating the user"
            }), 500

    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [],
                'message': SUCCESS_USER_CREATED
            }), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            'success': False,
            'status_code': 400,
            'data': [],
            'message': "Email and password are required."
        }), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({
            'success': False,
            'status_code': 401,
            'data': [],
            'message': "Invalid email or password."
        }), 401

    # Get the user's roles from the UserRoles table
    user_role = UserRoles.query.filter_by(user_id=user.id).first()
    role_name = Role.query.filter_by(id=user_role.role_id).first().name if user_role else "No Role Assigned"

    # Generate access token with user details
    access_token = create_access_token(identity={'user_id': user.id, 'email': user.email})

    # Include user details in the response
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'contact_no': user.contact_no,
        'status': user.status,
        'user_type': user.user_type,
        'work_location_type': user.work_location_type,
        'role': role_name,  # Add role information here
    }

    return jsonify({
        'success': True,
        'status_code': 200,
        'data': {
            'userInfo': user_data,
            'token': access_token
        },
        'message': "Logged in successfully!"
    }), 200



@auth_blueprint.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"response": ERROR_USER_NOT_FOUND}), 404
    return jsonify({"id": user.id, 'username': user.username, "email": user.email, "contact_no": user.contact_no,"user_type":user.user_type, "work_location_type":user.work_location_type, "status":user.status}), 200

@auth_blueprint.route('/user/edit/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user(user_id):
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    contact_no = data.get('contact_no')
    user_type = data.get('user_type')
    work_location_type = data.get('work_location_type')

    if not username or not email or not contact_no:
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': ERROR_MISSING_FIELDS
            }), 400

    if not is_valid_email(email):
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': ERROR_INVALID_EMAIL
            }), 400

    if not is_valid_contact(contact_no):
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': ERROR_INVALID_CONTACT
            }), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': ERROR_USER_NOT_FOUND
            }), 404

    # Check for unique constraints before updating
    existing_user_with_email = User.query.filter_by(email=email).first()
    existing_user_with_contact_no = User.query.filter_by(contact_no=contact_no).first()
    if existing_user_with_email and existing_user_with_email.id != user_id:
        return jsonify({
                'success': False,
                'status_code': 409,
                'data': [],
                'message': ERROR_USER_EXISTS_EMAIL
            }), 409
    if existing_user_with_contact_no and existing_user_with_contact_no.id != user_id:
        return jsonify({
                'success': False,
                'status_code': 409,
                'data': [],
                'message': ERROR_USER_EXISTS_CONTACTNO
            }), 409

    user.email = email
    user.username = username
    user.contact_no = contact_no
    user.user_type = user_type
    user.work_location_type = work_location_type

    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [],
                'message': SUCCESS_USER_UPDATED
            }), 200

@auth_blueprint.route('/user/reset-password', methods=['PUT'])
@jwt_required()
def update_password():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Email and new password are required"
            }), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "User with this email does not exist"
            }), 404

    # Updating the user's password
    user.set_password(password)
    db.session.commit()

    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [],
                'message': "Password updated successfully"
            }), 200

@auth_blueprint.route('/get/users/master-data', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    users_data = []
    
    for user in users:
        user_info = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "educations": {
                "university_name": user.education.university_name if user.education else None,
                "course_name": user.education.course_name if user.education else None,
                "start_date": user.education.start_date if user.education else None,
                "end_date": user.education.end_date if user.education else None,
                "grade": user.education.grade if user.education else None,
            },
            "personal": {
                "gender": user.personal.gender if user.personal else None,
                "dob": user.personal.dob if user.personal else None,
                "bio": user.personal.bio if user.personal else None,
                "address": user.personal.address if user.personal else None,
                "city": user.personal.city if user.personal else None,
                "state": user.personal.state if user.personal else None,
                "country": user.personal.country if user.personal else None,
                "zipcode": user.personal.zipcode if user.personal else None,
            },
            "professional": {
                "designation": user.professional.designation if user.professional else None,
                "prev_experience": user.professional.prev_experience if user.professional else None,
                "experience": user.professional.experience if user.professional else None,
                "salary": user.professional.salary if user.professional else None,
                "skills": user.professional.skills if user.professional else None,
                "cv_intro": user.professional.cv_intro if user.professional else None,
                "joining_date": user.professional.joining_date if user.professional else None,
                "permanent_confirm_date": user.professional.permanent_confirm_date if user.professional else None,
                "termination_date": user.professional.termination_date if user.professional else None,
                "termination_reason": user.professional.termination_reason if user.professional else None,
            },
            "bank": {
                "account_number": user.bank.account_number if user.bank else None,
                "ifsc_code": user.bank.ifsc_code if user.bank else None,
                "bank_name": user.bank.bank_name if user.bank else None,
                "branch_name": user.bank.branch_name if user.bank else None,
            }
        }
        users_data.append(user_info)
    
    return jsonify(users_data)