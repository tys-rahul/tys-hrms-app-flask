from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.project import Project
from flask_jwt_extended import jwt_required

project_blueprint = Blueprint('projects', __name__)

# Get All Projects
@project_blueprint.route('/get/all-users/project/list', methods=['GET'])
@jwt_required()
def get_projects():
    projects = Project.query.all()
    project_list = [project.to_dict() for project in projects]
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [project_list],
                'message': "Data fetched successfully!"
            }), 200

# Get Project by ID
@project_blueprint.route('/get/user/project-details/<int:id>', methods=['GET'])
@jwt_required()
def get_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({
            'success': False,
            'status_code': 404,
            'data': [],
            'message': "No project found with the given ID."
        }), 404

    return jsonify({
        'success': True,
        'status_code': 200,
        'data': [project.to_dict()],
        'message': "Data fetched successfully!"
    }), 200
    
# Get Projects by User ID
@project_blueprint.route('/get/user/project/list/<int:user_id>', methods=['GET'])
@jwt_required()
def get_project_by_userId(user_id):
    projects = Project.query.filter_by(user_id=user_id).all()
    
    if not projects:
        return jsonify({
            'success': False,
            'status_code': 404,
            'data': [],
            'message': "No projects found for the given user ID."
        }), 404

    return jsonify({
        'success': True,
        'status_code': 200,
        'data': [project.to_dict() for project in projects],
        'message': "Data fetched successfully!"
    }), 200


# Create Project
@project_blueprint.route('/add/user/project-details', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()
    new_project = Project(**data)
    db.session.add(new_project)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [new_project.to_dict()],
                'message': "Project created successfully!"
            }), 201

# Update Project
@project_blueprint.route('/update/user/project-details/<int:id>', methods=['PUT'])
@jwt_required()
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(project, key, value)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [project.to_dict()],
                'message': "Data updated successfully!"
            }), 200

# Delete Project
@project_blueprint.route('/delete/user/project-details/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [],
                'message': "Project deleted  successfully!"
            }), 200


def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
Project.to_dict = to_dict