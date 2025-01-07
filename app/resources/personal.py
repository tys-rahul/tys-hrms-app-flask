from flask import Blueprint, jsonify, request
from app.extensions import db
from datetime import datetime
from app.models.personal import Personal
from flask_jwt_extended import jwt_required

personal_blueprint = Blueprint('personal', __name__)

@personal_blueprint.route('/get/all-users/personal/list', methods=['GET'])
@jwt_required()
def get_personals():
    personals = Personal.query.all()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [personal.to_dict() for personal in personals],
                'message': "Data fetched successfully!"
            }), 200

@personal_blueprint.route('/get/user/personal-details/<int:user_id>', methods=['GET'])
@jwt_required()
def get_personal(user_id):
    personal = Personal.query.filter_by(user_id=user_id).first()
    
    if not personal:
        return jsonify({
            'success': False,
            'status_code': 404,
            'message': "No personal details found for the given user ID."
        }), 404

    return jsonify({
        'success': True,
        'status_code': 200,
        'data': [personal.to_dict()],
        'message': "Data fetched successfully!"
    }), 200

@personal_blueprint.route('/add/user/personal-details', methods=['POST'])
@jwt_required()
def create_personal():
    data = request.get_json()

    if 'dob' in data:
        data['dob'] = datetime.strptime(data['dob'], '%Y-%m-%d').date()

    new_personal = Personal(**data)
    db.session.add(new_personal)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [new_personal.to_dict()],
                'message': "Data created successfully!"
            }), 201

@personal_blueprint.route('/update/user/personal-details/<int:id>', methods=['PUT'])
@jwt_required()
def update_personal(id):
    personal = Personal.query.get_or_404(id)
    data = request.get_json()

    if 'dob' in data:
        data['dob'] = datetime.strptime(data['dob'], '%Y-%m-%d').date()

    for key, value in data.items():
        setattr(personal, key, value)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [personal.to_dict()],
                'message': "Data updated successfully!"
            }), 200
    
@personal_blueprint.route('/delete/user/personal-details/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_personal(id):
    personal = Personal.query.get_or_404(id)
    db.session.delete(personal)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [],
                'message': "Data deleted successfully!"
            }), 200

def to_dict(self):
    return {
        "id": self.id,
        "src": self.src,
        "mime_type": self.mime_type,
        "gender": self.gender,
        "dob": self.dob.isoformat() if self.dob else None,
        "bio": self.bio,
        "address": self.address,
        "address2": self.address2,
        "state": self.state,
        "city": self.city,
        "zipcode": self.zipcode,
        "country": self.country,
        "address_type": self.address_type,
        "user_id": self.user_id,
    }

Personal.to_dict = to_dict
