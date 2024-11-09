from flask import Blueprint, request, jsonify
from app.models.leaves import Leave
from app.extensions import db
from datetime import datetime
from flask_jwt_extended import jwt_required

leaves_blueprint = Blueprint('leaves', __name__)

@leaves_blueprint.route('/add/user/leave/request', methods=['POST'])
@jwt_required()
def create_leave():
    data = request.json
    try:
        end_date = data.get('end_date')
        leave_type = "AL" if not end_date else "FL"
        
        new_leave = Leave(
            user_id=data['user_id'],
            email=data['email'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None,
            reason=data.get('reason', 'NA'),
            comment=data.get('comment', 'NA'),
            status=data.get('status', 'Pending'),
            applied_on=datetime.now().date(),
            label=data.get('label', 'LV'),
            leave_type=leave_type
        )

        db.session.add(new_leave)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'status_code': 201,
            'data': leave_to_dict(new_leave),
            'message': "Leave created successfully!"
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'status_code': 400,
            'error': str(e),
            'message': "An error occurred while creating the leave request."
        }), 400

@leaves_blueprint.route('/get/user/leave/request/<int:id>', methods=['GET'])
@jwt_required()
def get_leave(id):
    leave = Leave.query.get(id)
    if leave:
        return jsonify({
            'success': True,
            'status_code': 200,
            'data': leave_to_dict(leave),
            'message': "Leave fetched successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'error': "Leave not found",
        'message': "Leave not found"
    }), 404

@leaves_blueprint.route('/get/all-users/leave/list', methods=['GET'])
@jwt_required()
def get_all_leaves():
    leaves = Leave.query.all()
    return jsonify({
        'success': True,
        'status_code': 200,
        'data': [leave_to_dict(leave) for leave in leaves],
        'message': "Data fetched successfully!"
    }), 200

@leaves_blueprint.route('/get/user/leave-request/userId/<int:user_id>', methods=['GET'])
@jwt_required()
def get_leaves_by_user_id(user_id):
    leaves = Leave.query.filter_by(user_id=user_id).all()
    return jsonify({
        'success': True,
        'status_code': 200,
        'data': [leave_to_dict(leave) for leave in leaves],
        'message': "User's leave data fetched successfully!"
    }), 200

@leaves_blueprint.route('/update/user/leave-request/<int:id>', methods=['PUT'])
@jwt_required()
def update_leave(id):
    data = request.json
    leave = Leave.query.get(id)
    if leave:
        leave.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date() if data.get('end_date') else None
        leave.leave_type = "AL" if not leave.end_date else "FL"
        leave.reason = data.get('reason', leave.reason)
        leave.comment = data.get('comment', leave.comment)
        leave.status = data.get('status', leave.status)
        leave.label = data.get('label', leave.label)

        db.session.commit()
        return jsonify({
            'success': True,
            'status_code': 200,
            'data': leave_to_dict(leave),
            'message': "Leave updated successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'error': "Leave not found",
        'message': "Leave not found"
    }), 404

@leaves_blueprint.route('/delete/user/leave-request/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_leave(id):
    leave = Leave.query.get(id)
    if leave:
        db.session.delete(leave)
        db.session.commit()
        return jsonify({
            'success': True,
            'status_code': 200,
            'message': "Leave deleted successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'error': "Leave not found",
        'message': "Leave not found"
    }), 404

def leave_to_dict(leave):
    return {
        "id": leave.id,
        "user_id": leave.user_id,
        "email": leave.email,
        "start_date": leave.start_date.strftime('%Y-%m-%d') if leave.start_date else None,
        "end_date": leave.end_date.strftime('%Y-%m-%d') if leave.end_date else None,
        "reason": leave.reason,
        "comment": leave.comment,
        "status": leave.status,
        "applied_on": leave.applied_on.strftime('%Y-%m-%d') if leave.applied_on else None,
        "label": leave.label,
        "leave_type": leave.leave_type,
        "created_at": leave.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": leave.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    }
