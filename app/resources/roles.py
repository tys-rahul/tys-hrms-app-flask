from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.role import Role, Permission, RolePermissions
from app.utils.decorators import permission_required

roles_blueprint = Blueprint('roles', __name__)

@roles_blueprint.route('/roles', methods=['POST'])
# @jwt_required()
# @permission_required('view_admin_dashboard')
def create_role():
    data = request.get_json()
    role_name = data.get('name')

    if Role.query.filter_by(name=role_name).first():
        return jsonify({"response": "Role already exists"}), 400

    new_role = Role(name=role_name)
    db.session.add(new_role)
    db.session.commit()

    return jsonify({"response": "Role created successfully"}), 201

@roles_blueprint.route('/permissions', methods=['POST'])
def create_permission():
    data = request.get_json()
    permission_name = data.get('name')

    if Permission.query.filter_by(name=permission_name).first():
        return jsonify({"response": "Permission already exists"}), 400

    new_permission = Permission(name=permission_name)
    db.session.add(new_permission)
    db.session.commit()

    return jsonify({"response": "Permission created successfully"}), 201

@roles_blueprint.route('/roles/<int:role_id>/permissions', methods=['POST'])
def assign_permissions_to_role(role_id):
    data = request.get_json()
    permission_ids = data.get('permission_ids')

    role = Role.query.get(role_id)
    if not role:
        return jsonify({"response": "Role not found"}), 404

    for permission_id in permission_ids:
        permission = Permission.query.get(permission_id)
        if permission and permission not in role.permissions:
            role.permissions.append(permission)

    db.session.commit()
    return jsonify({"response": "Permissions assigned successfully"}), 200
