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
    return jsonify(project_list), 200

# Get Project by ID
@project_blueprint.route('/get/user/project-details/<int:id>', methods=['GET'])
@jwt_required()
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify(project.to_dict()), 200

# Create Project
@project_blueprint.route('/add/user/project-details', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()
    new_project = Project(**data)
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201

# Update Project
@project_blueprint.route('/update/user/project-details/<int:id>', methods=['PUT'])
@jwt_required()
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(project, key, value)
    db.session.commit()
    return jsonify(project.to_dict()), 200

# Delete Project
@project_blueprint.route('/delete/user/project-details/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200


def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
Project.to_dict = to_dict