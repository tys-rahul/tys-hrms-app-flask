from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.education import Education
from flask_jwt_extended import jwt_required

education_blueprint = Blueprint('education', __name__)

@education_blueprint.route('/get/all-users/education/list', methods=['GET'])
@jwt_required()
def get_educations():
    educations = Education.query.all()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [education.to_dict() for education in educations],
                'message': "Data fetched successfully!"
            }), 200

@education_blueprint.route('/get/user/education-details/<int:id>', methods=['GET'])
@jwt_required()
def get_education(id):
    education = Education.query.get_or_404(id)
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [education.to_dict()],
                'message': "Data fetched successfully!"
            }), 200

@education_blueprint.route('/get/user/education-list/<int:user_id>', methods=['GET'])
@jwt_required()
def get_education_list(user_id):
    
    education_records = Education.query.filter_by(user_id=user_id).all()
    education_data = [record.to_dict() for record in education_records]
    
    return jsonify({
        'success': True,
        'status_code': 200,
        'data': education_data,
        'message': "Data fetched successfully!"
    }), 200

@education_blueprint.route('/add/user/education-details', methods=['POST'])
@jwt_required()
def create_education():
    data = request.get_json()
    new_education = Education(**data)
    db.session.add(new_education)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [new_education.to_dict()],
                'message': "Data created successfully!"
            }), 201

@education_blueprint.route('/update/user/education-details/<int:id>', methods=['PUT'])
@jwt_required()
def update_education(id):
    education = Education.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(education, key, value)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [education.to_dict()],
                'message': "Data updated successfully!"
            }), 200

@education_blueprint.route('/delete/user/education-details/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_education(id):
    education = Education.query.get_or_404(id)
    db.session.delete(education)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 204,
                'data': [],
                'message': "Data deleted successfully!"
            }), 204

def to_dict(self):
    return {
        "id": self.id,
        "university_name": self.university_name,
        "course_name": self.course_name,
        "start_date": self.start_date,
        "end_date": self.end_date,
        "grade": self.grade,
        "user_id": self.user_id,
    }

Education.to_dict = to_dict
