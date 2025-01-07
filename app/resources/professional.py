from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.professional import Professional
from flask_jwt_extended import jwt_required

professional_blueprint = Blueprint('professional', __name__)

@professional_blueprint.route('/get/all-users/professional/list', methods=['GET'])
@jwt_required()
def get_professionals():
    professionals = Professional.query.all()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [professional.to_dict() for professional in professionals],
                'message': "Data fetched successfully!"
            }), 200

@professional_blueprint.route('/get/user/professional-details/<int:user_id>', methods=['GET'])
@jwt_required()
def get_professional(user_id):
    professional = Professional.query.filter_by(user_id=user_id).first()
    
    if not professional:
        return jsonify({
            'success': False,
            'status_code': 404,
            'message': "No professional details found for the given user ID."
        }), 404

    return jsonify({
        'success': True,
        'status_code': 200,
        'data': [professional.to_dict()], 
        'message': "Data fetched successfully!"
    }), 200

@professional_blueprint.route('/add/user/professional-details', methods=['POST'])
@jwt_required()
def create_professional():
    data = request.get_json()
    new_professional = Professional(**data)
    db.session.add(new_professional)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [new_professional.to_dict()],
                'message': "Data created successfully!"
            }), 201

@professional_blueprint.route('/update/user/professional-details/<int:id>', methods=['PUT'])
@jwt_required()
def update_professional(id):
    professional = Professional.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(professional, key, value)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [professional.to_dict()],
                'message': "Data updated successfully!"
            }), 200

@professional_blueprint.route('/delete/user/professional-details/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_professional(id):
    professional = Professional.query.get_or_404(id)
    db.session.delete(professional)
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
        "designation": self.designation,
        "prev_experience": self.prev_experience,
        "experience": self.experience,
        "salary": self.salary,
        "skills": self.skills,
        "cv_intro": self.cv_intro,
        "joining_date": self.joining_date,
        "permanent_confirm_date": self.permanent_confirm_date,
        "termination_date": self.termination_date,
        "termination_reason": self.termination_reason,
        "user_id": self.user_id,
    }

Professional.to_dict = to_dict
