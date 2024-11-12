from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.leaves import Leave
from app.models.reimbursement import Reimbursement
from app.models.regularization import Regularization
from app.models.user import User
from app.models.personal import Personal
from app.models.professional import Professional
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.resources.regularizations import regularization_to_dict
from app.resources.leaves import leave_to_dict
from app.resources.reimbursement import reimbursement_to_dict
from datetime import datetime

notification_blueprint = Blueprint('notifications', __name__)

@notification_blueprint.route('/get/admin/notification', methods=['GET'])
@jwt_required()
def fetch_notifications():
    app_data = {}

    regularizations = (
        db.session.query(Regularization, Personal.src)
        .join(Personal, Regularization.user_id == Personal.user_id, isouter=True)
        .filter(Regularization.status == 'Pending')
        .order_by(Regularization.id.desc())
        .all()
    )

    leaves = (
        db.session.query(Leave, Personal.src)
        .join(Personal, Leave.user_id == Personal.user_id, isouter=True)
        .filter(Leave.status == 'Pending')
        .order_by(Leave.id.desc())
        .all()
    )

    reimbursements = (
        db.session.query(Reimbursement, Personal.src)
        .join(Personal, Reimbursement.user_id == Personal.user_id, isouter=True)
        .filter(Reimbursement.status == 'Pending')
        .order_by(Reimbursement.id.desc())
        .all()
    )

    sorted_data = [
       {'type': 'regularization', **regularization_to_dict(r.Regularization), 'src': r.src}
        for r in regularizations
    ] + [
        {'type': 'leave', **leave_to_dict(l.Leave), 'src': l.src} for l in leaves
    ] + [
        {'type': 'reimbursement', **reimbursement_to_dict(rm.Reimbursement), 'src': rm.src} for rm in reimbursements
    ]

    for data in sorted_data:
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')

    sorted_data = sorted(sorted_data, key=lambda x: x.get('created_at'), reverse=True)

    for data in sorted_data:
        if isinstance(data.get('created_at'), datetime):
            data['created_at'] = data['created_at'].strftime('%Y-%m-%d %H:%M:%S')

    app_data['notification'] = sorted_data

    reg_count = db.session.query(Regularization).filter_by(status='Pending').count()
    leave_count = db.session.query(Leave).filter_by(status='Pending').count()
    reimbursement_count = db.session.query(Reimbursement).filter_by(status='Pending').count()

    app_data['notificationCount'] = reg_count + leave_count + reimbursement_count

    current_user = get_jwt_identity().get('user_id')
    
    # Fetch User Identity
    user_identity = (
        db.session.query(
            User.id.label('user_id'),  
            User.username,
            User.contact_no,
            User.email,
            Personal.src,
            Personal.gender,
            Personal.dob,
            Professional.designation,
            Professional.joining_date
        )
        .join(Personal, User.id == Personal.user_id, isouter=True)
        .join(Professional, User.id == Professional.user_id, isouter=True)
        .filter(User.id == current_user)  
        .first()
    )

    if user_identity:
        app_data['user_identity'] = {
            'user_id': user_identity.user_id,
            'username': user_identity.username,
            'contact_no': user_identity.contact_no,
            'email': user_identity.email,
            'src': user_identity.src,
            'gender': user_identity.gender,
            'dob': user_identity.dob,
            'designation': user_identity.designation,
            'joining_date': user_identity.joining_date
        }
    else:
        app_data['error'] = 'User not found'

    return jsonify({
            'success': True,
            'status_code': 200,
            'data': app_data,
            'message': 'Notification record fetched successfully!'
        }), 200
