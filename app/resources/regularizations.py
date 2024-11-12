from flask import Blueprint, request, jsonify
from app.models.regularization import Regularization
from app.models.user import User
from app.models.attendance import Attendance
from app.extensions import db
from datetime import datetime, timezone
from flask_jwt_extended import jwt_required

regularization_blueprint = Blueprint('regularizations', __name__)

@regularization_blueprint.route('/add/user/regularization', methods=['POST'])
@jwt_required()
def create_regularization():
    data = request.json
    try:
        user_id = data.get('user_id')
        att_id = data.get('att_id')
        email = data.get('email')
        att_date_str = data.get('att_date')
        reason = data.get('reason')
        comment = data.get('comment', 'NA')
        status = data.get('status', 'Pending')
        label = data.get('label', 'RG')

        # Validate user_id and att_id if provided
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return jsonify({
                    'success': False,
                    'status_code': 404,
                    'message': "User not found"
                }), 404

        if att_id:
            attendance = Attendance.query.get(att_id)
            if not attendance:
                return jsonify({
                    'success': False,
                    'status_code': 404,
                    'message': "Attendance record not found"
                }), 404

        # Parse att_date
        att_date = datetime.strptime(att_date_str, '%Y-%m-%d').date() if att_date_str else None

        # Check if a regularization request for the same user and att_date already exists
        existing_regularization = Regularization.query.filter_by(user_id=user_id, att_date=att_date).first()
        if existing_regularization:
            return jsonify({
                'success': False,
                'status_code': 400,
                'message': "A regularization request already exists for this user and date."
            }), 400

        new_regularization = Regularization(
            user_id=user_id,
            att_id=att_id,
            email=email,
            att_date=att_date,
            reason=reason,
            comment=comment,
            status=status,
            label=label
        )

        db.session.add(new_regularization)
        db.session.commit()

        return jsonify({
            'success': True,
            'status_code': 201,
            'data': regularization_to_dict(new_regularization),
            'message': "Regularization created successfully"
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'status_code': 400,
            'message': str(e)
        }), 400
@regularization_blueprint.route('/get/user/regularization/<int:id>', methods=['GET'])
@jwt_required()
def get_regularization(id):
    regularization = Regularization.query.get(id)
    if regularization:
        return jsonify({
            'success': True,
            'status_code': 200,
            'data': regularization_to_dict(regularization),
            'message': "Data fetched successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'message': "Regularization not found"
    }), 404

@regularization_blueprint.route('/get/all-users/regularization/list', methods=['GET'])
@jwt_required()
def get_all_regularizations():
    regularizations = Regularization.query.all()
    data = [regularization_to_dict(reg) for reg in regularizations]
    return jsonify({
        'success': True,
        'status_code': 200,
        'data': data,
        'message': "Data fetched successfully!"
    }), 200

@regularization_blueprint.route('/update/user/regularization/<int:id>', methods=['PUT'])
@jwt_required()
def update_regularization(id):
    data = request.json
    regularization = Regularization.query.get(id)
    if regularization:
        try:
            user_id = data.get('user_id', regularization.user_id)
            att_id = data.get('att_id', regularization.att_id)
            email = data.get('email', regularization.email)
            att_date_str = data.get('att_date')
            reason = data.get('reason', regularization.reason)
            comment = data.get('comment', regularization.comment)
            status = data.get('status', regularization.status)
            label = data.get('label', regularization.label)

            # Validate user_id and att_id if provided
            if user_id:
                user = User.query.get(user_id)
                if not user:
                    return jsonify({
                        'success': False,
                        'status_code': 404,
                        'message': "User not found"
                    }), 404
                regularization.user_id = user_id

            if att_id:
                attendance = Attendance.query.get(att_id)
                if not attendance:
                    return jsonify({
                        'success': False,
                        'status_code': 404,
                        'message': "Attendance record not found"
                    }), 404
                regularization.att_id = att_id

            # Parse att_date
            if att_date_str:
                att_date = datetime.strptime(att_date_str, '%Y-%m-%d').date()
                regularization.att_date = att_date

            regularization.email = email
            regularization.reason = reason
            regularization.comment = comment
            regularization.status = status
            regularization.label = label

            db.session.commit()
            return jsonify({
                'success': True,
                'status_code': 200,
                'data': regularization_to_dict(regularization),
                'message': "Regularization updated successfully"
            }), 200

        except Exception as e:
            return jsonify({
                'success': False,
                'status_code': 400,
                'message': str(e)
            }), 400

    return jsonify({
        'success': False,
        'status_code': 404,
        'message': "Regularization not found"
    }), 404

@regularization_blueprint.route('/delete/user/regularization/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_regularization(id):
    regularization = Regularization.query.get(id)
    if regularization:
        try:
            db.session.delete(regularization)
            db.session.commit()
            return jsonify({
                'success': True,
                'status_code': 200,
                'message': "Regularization deleted successfully"
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'status_code': 400,
                'message': str(e)
            }), 400
    return jsonify({
        'success': False,
        'status_code': 404,
        'message': "Regularization not found"
    }), 404

@regularization_blueprint.route('/get/user/regularization-list/userId/<int:user_id>', methods=['GET'])
@jwt_required()
def get_regularizations_by_user(user_id):
    regularizations = Regularization.query.filter_by(user_id=user_id).all()
    if regularizations:
        return jsonify({
            'success': True,
            'status_code': 200,
            'data': [regularization_to_dict(reg) for reg in regularizations],
            'message': "Data fetched successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'message': "No regularizations found for this user"
    }), 404

def regularization_to_dict(regularization):
    return {
        "id": regularization.id,
        "user_id": regularization.user_id,
        "att_id": regularization.att_id,
        "email": regularization.email,
        "att_date": regularization.att_date.strftime('%Y-%m-%d') if regularization.att_date else None,
        "reason": regularization.reason,
        "comment": regularization.comment,
        "status": regularization.status,
        "label": regularization.label,
        "created_at": regularization.created_at.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": regularization.updated_at.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    }
