from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models.user import User

def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = User.query.filter_by(username=get_jwt_identity()).first()

            user_permissions = [perm.name for role in current_user.roles for perm in role.permissions]

            if permission_name not in user_permissions:
                return jsonify({"response": "Permission denied"}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator
