from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import jwt_required
from app.utils.decorators import permission_required

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/update/user-status/<int:user_id>', methods=['PUT'])
@jwt_required()
# @permission_required('update_user_status')  
def update_user_status(user_id):
    data = request.get_json()
    status = data.get('status')

    if status not in [0, 1]:
        return jsonify({"response": "Status must be either 0 or 1"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"response": "User not found"}), 404

    user.status = status
    db.session.commit()

    if status == 0:
        return jsonify({"response": "User activated successfully"}), 200
    else:
        return jsonify({"response": "User deactivated successfully"}), 200

@admin_blueprint.route('/get/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    return jsonify([{"id": user.id, 'username': user.username, "email": user.email, "contact_no": user.contact_no, "status": user.status} for user in users]), 200


@admin_blueprint.route('/delete/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"response": ERROR_USER_NOT_FOUND}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"response": SUCCESS_USER_DELETED}), 200
