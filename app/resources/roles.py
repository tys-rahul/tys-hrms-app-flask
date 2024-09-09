from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.role import Role, Permission, RolePermissions, UserRoles
from app.models.user import User
from app.utils.decorators import permission_required
from flask_jwt_extended import jwt_required

roles_blueprint = Blueprint('roles', __name__)

@roles_blueprint.route('/add/user/role', methods=['POST'])
@jwt_required()
def create_role():
    data = request.get_json()
    role_name = data.get('name')

    if Role.query.filter_by(name=role_name).first():
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Role already exists"
            }), 400

    new_role = Role(name=role_name)
    db.session.add(new_role)
    db.session.commit()

    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [],
                'message': "Role created  successfully!"
            }), 201

@roles_blueprint.route('/add/user/permission', methods=['POST'])
@jwt_required()
def create_permission():
    data = request.get_json()
    permission_name = data.get('name')

    if Permission.query.filter_by(name=permission_name).first():
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Permission already exists"
            }), 400

    new_permission = Permission(name=permission_name)
    db.session.add(new_permission)
    db.session.commit()

    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [],
                'message': "Permission created successfully!"
            }), 201

@roles_blueprint.route('/assign/user/permission/<int:role_id>', methods=['POST'])
@jwt_required()
def assign_permissions_to_role(role_id):
    data = request.get_json()
    permission_ids = data.get('permission_ids')

    role = Role.query.get(role_id)
    if not role:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "Role not found"
            }), 404

    for permission_id in permission_ids:
        permission = Permission.query.get(permission_id)
        if permission and permission not in role.permissions:
            role.permissions.append(permission)

    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [],
                'message': "Permissions assigned  successfully!"
            }), 201

@roles_blueprint.route('/assign/user/role', methods=['POST'])
def add_user_role():
    data = request.get_json()
    
    user_id = data.get('user_id')
    role_id = data.get('role_id')

    if not user_id or not role_id:
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "User ID and Role ID are required"
            }), 400

    user = User.query.get(user_id)
    role = Role.query.get(role_id)

    if not user or not role:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "User or Role not found"
            }), 404

    # Check if the role is already assigned to the user
    existing_user_role = UserRoles.query.filter_by(user_id=user_id, role_id=role_id).first()
    if existing_user_role:
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Role already assigned to the user"
            }), 400

    # Assign the role to the user
    user_role = UserRoles(user_id=user_id, role_id=role_id)
    db.session.add(user_role)
    db.session.commit()

    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [],
                'message': "Role assigned successfully!"
            }), 201

@roles_blueprint.route('/get/assigned/user-roles', methods=['GET'])
def get_user_roles():
    user_roles = UserRoles.query.all()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [ {"user_id": user_role.user_id, "role_id": user_role.role_id} for user_role in user_roles],
                'message': "Data fetched successfully!"
            }), 200

@roles_blueprint.route('/get/assigned/user-role/<int:user_id>', methods=['GET'])
def get_user_roles_by_id(user_id):
    user_roles = UserRoles.query.filter_by(user_id=user_id).all()

    if not user_roles:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "No roles found for this user"
            }), 404

    roles = []
    for user_role in user_roles:
        role = Role.query.get(user_role.role_id)
        roles.append({'role_id': role.id, 'role_name': role.name})

    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [{'user_id': user_id, 'roles': roles}],
                'message': "Data fetched successfully!"
            }), 200


@roles_blueprint.route('/get/user/roles-list', methods=['GET'])
@jwt_required()
def get_all_roles():
    roles = Role.query.all()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [{"id": role.id, 'name': role.name} for role in roles],
                'message': "Data fetched successfully!"
            }), 200

@roles_blueprint.route('/get/user/permissions', methods=['GET'])
@jwt_required()
def get_all_permissions():
    roles = Permission.query.all()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [{"id": role.id, 'name': role.name} for role in roles],
                'message': "Data fetched successfully!"
            }), 200

@roles_blueprint.route('/get/user/assigned-roles', methods=['GET'])
@jwt_required()
def get_all_assigned_roles():
    rolePermissions = RolePermissions.query.all()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [{"role_id": rolePrm.role_id, 'permission_id': rolePrm.permission_id} for rolePrm in rolePermissions],
                'message': "Data fetched successfully!"
            }), 200
