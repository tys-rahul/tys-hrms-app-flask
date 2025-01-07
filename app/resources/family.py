from flask import Flask, request, jsonify
from datetime import datetime
from flask import Blueprint, jsonify, request
from app.models.user import User
from app.models.family import Family
from app.extensions import db
from flask_jwt_extended import jwt_required

family_blueprint = Blueprint('family', __name__)

# Get all family details (optional: filter by user)
@family_blueprint.route('/get/all-users/family/list', methods=['GET'])
@jwt_required()
def get_all_families():
    user_id = request.args.get('user_id')
    if user_id:
        families = Family.query.filter_by(user_id=user_id).all()
    else:
        families = Family.query.all()

    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [family.to_dict() for family in families],
                'message': "Data fetched successfully!"
            }), 200

# Get family details by family ID
@family_blueprint.route('/get/user/family-details/<int:user_id>', methods=['GET'])
@jwt_required()
def get_family(user_id):
    family_details = Family.query.filter_by(user_id=user_id).all()

    if not family_details:
        return jsonify({
            'success': False,
            'status_code': 404,
            'data': [],
            'message': "No family details found for the given user ID."
        }), 404

    data = [family.to_dict() for family in family_details]

    return jsonify({
        'success': True,
        'status_code': 200,
        'data': data,
        'message': "Data fetched successfully!"
    }), 200

# Create a new family entry
@family_blueprint.route('/add/user/family-details', methods=['POST'])
@jwt_required()
def create_family():
    data = request.get_json()
    user_id = data.get('user_id')

    # Ensure user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "User not found"
            }), 404

    new_family = Family(**data)
    db.session.add(new_family)
    db.session.commit()

    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [new_family.to_dict()],
                'message': "Data created successfully!"
            }), 201

# Update family details
@family_blueprint.route('/update/user/family-details/<int:id>', methods=['PUT'])
@jwt_required()
def update_family(id):
    family = Family.query.get(id)
    if not family:
        return jsonify({"error": "Family not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(family, key, value)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [family.to_dict()],
                'message': "Data updated successfully!"
            }), 200

# Delete family entry
@family_blueprint.route('/delete/user/family-details/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_family(id):
    family = Family.query.get(id)
    if not family:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "Family not found"
            }), 404

    db.session.delete(family)
    db.session.commit()

    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [],
                'message': "Family entry deleted successfully"
            }), 200

def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'personal_email': self.personal_email,
            'alternate_contact': self.alternate_contact,
            'family_address': self.family_address,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
Family.to_dict = to_dict