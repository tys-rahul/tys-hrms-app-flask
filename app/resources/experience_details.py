from flask import Blueprint, request, jsonify
from app.models.experience_details import ExperienceDetails
from app.extensions import db
from datetime import datetime, timezone
from flask_jwt_extended import jwt_required

experience_blueprint = Blueprint('experience', __name__)

@experience_blueprint.route('/get/all-users/experience/list', methods=['GET'])
@jwt_required()
def get_all_experience():
    experiences = ExperienceDetails.query.all()
    data = [experience_to_dict(experience) for experience in experiences]
    return jsonify({
        'success': True,
        'status_code': 200,
        'data': data,
        'message': "Data fetched successfully!"
    }), 200

@experience_blueprint.route('/add/user/experience', methods=['POST'])
@jwt_required()
def create_experience():
    data = request.json
    try:
        user_id = data.get('user_id')
        company_name = data.get('company_name')
        designation = data.get('designation')
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
        end_date = data.get('end_date')
        experience = data.get('experience')
        
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        new_experience = ExperienceDetails(
            user_id=user_id,
            company_name=company_name,
            designation=designation,
            start_date=start_date,
            end_date=end_date,
            experience=experience
        )
        
        db.session.add(new_experience)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'status_code': 201,
            'data': experience_to_dict(new_experience),
            'message': "Experience created successfully!"
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'status_code': 400,
            'data': None,
            'message': str(e)
        }), 400

@experience_blueprint.route('/get/user/experience/<int:id>', methods=['GET'])
@jwt_required()
def get_experience(id):
    experience = ExperienceDetails.query.get(id)
    if experience:
        return jsonify({
            'success': True,
            'status_code': 200,
            'data': experience_to_dict(experience),
            'message': "Data fetched successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'data': None,
        'message': "Experience not found"
    }), 404

@experience_blueprint.route('/update/user/experience/<int:id>', methods=['PUT'])
@jwt_required()
def update_experience(id):
    data = request.json
    experience = ExperienceDetails.query.get(id)
    if experience:
        experience.company_name = data.get('company_name', experience.company_name)
        experience.designation = data.get('designation', experience.designation)
        experience.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d') if data.get('start_date') else experience.start_date
        experience.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d') if data.get('end_date') else experience.end_date
        experience.experience = data.get('experience', experience.experience)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'status_code': 200,
            'data': experience_to_dict(experience),
            'message': "Experience updated successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'data': None,
        'message': "Experience not found"
    }), 404

@experience_blueprint.route('/delete/user/experience/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_experience(id):
    experience = ExperienceDetails.query.get(id)
    if experience:
        db.session.delete(experience)
        db.session.commit()
        return jsonify({
            'success': True,
            'status_code': 200,
            'data': None,
            'message': "Experience deleted successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'data': None,
        'message': "Experience not found"
    }), 404

@experience_blueprint.route('/get/user/experiences/userId/<int:user_id>', methods=['GET'])
@jwt_required()
def get_experiences_by_user(user_id):
    experiences = ExperienceDetails.query.filter_by(user_id=user_id).all()
    if experiences:
        return jsonify({
            'success': True,
            'status_code': 200,
            'data': [experience_to_dict(exp) for exp in experiences],
            'message': "Data fetched successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'data': None,
        'message': "No experiences found for this user"
    }), 404

def experience_to_dict(experience):
    return {
        "id": experience.id,
        "user_id": experience.user_id,
        "company_name": experience.company_name,
        "designation": experience.designation,
        "start_date": experience.start_date.strftime('%Y-%m-%d'),
        "end_date": experience.end_date.strftime('%Y-%m-%d') if experience.end_date else None,
        "experience": experience.experience,
        "created_at": experience.created_at.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": experience.updated_at.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    }
