from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.reimbursement import Reimbursement
from flask_jwt_extended import jwt_required
from datetime import date

reimbursement_blueprint = Blueprint('reimbursements', __name__)


# Create Reimbursement
@reimbursement_blueprint.route('/add/user/reimbursement', methods=['POST'])
@jwt_required()
def create_reimbursement():
    data = request.get_json()
    reimbursement = Reimbursement(
        user_id=data.get('user_id'),
        email=data.get('email'),
        upi_id=data.get('upi_id'),
        expense_date=date.fromisoformat(data.get('expense_date')),
        expense_item=data.get('expense_item'),
        expense_cost=data.get('expense_cost'),
        quantity=data.get('quantity'),
        sum=data.get('sum'),
        receipt=data.get('receipt', 'NA'),
        total_amt=data.get('total_amt'),
        ref_no=data.get('ref_no', 'NA'),
        status=data.get('status', 'Pending'),
        label=data.get('label', 'RM')
    )
    db.session.add(reimbursement)
    db.session.commit()
    return jsonify({
        'success': True,
        'status_code': 201,
        'data': reimbursement_to_dict(reimbursement),
        'message': "Reimbursement created successfully!"
    }), 201

# Get Reimbursement by ID
@reimbursement_blueprint.route('/get/user/reimbursement/<int:id>', methods=['GET'])
@jwt_required()
def get_reimbursement(id):
    reimbursement = Reimbursement.query.get_or_404(id)
    return jsonify({
        'success': True,
        'status_code': 200,
        'data': reimbursement_to_dict(reimbursement),
        'message': "Reimbursement fetched successfully!"
    }), 200

# Update Reimbursement
@reimbursement_blueprint.route('/update/user/reimbursement/<int:id>', methods=['PUT'])
@jwt_required()
def update_reimbursement(id):
    data = request.get_json()
    reimbursement = Reimbursement.query.get_or_404(id)

    for key, value in data.items():
        if hasattr(reimbursement, key):
            setattr(reimbursement, key, value)

    db.session.commit()
    return jsonify({
        'success': True,
        'status_code': 200,
        'data': reimbursement_to_dict(reimbursement),
        'message': "Reimbursement updated successfully!"
    }), 200

# Delete Reimbursement
@reimbursement_blueprint.route('/delete/user/reimbursement/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_reimbursement(id):
    reimbursement = Reimbursement.query.get_or_404(id)
    db.session.delete(reimbursement)
    db.session.commit()
    return jsonify({
        'success': True,
        'status_code': 200,
        'message': "Reimbursement deleted successfully!"
    }), 200

# Fetch Reimbursements by User ID
@reimbursement_blueprint.route('/get/reimbursements/userId/<string:user_id>', methods=['GET'])
@jwt_required()
def get_reimbursements_by_user_id(user_id):
    reimbursements = Reimbursement.query.filter_by(user_id=user_id).all()
    reimbursements_data = [reimbursement_to_dict(reimbursement) for reimbursement in reimbursements]
    return jsonify({
        'success': True,
        'status_code': 200,
        'data': reimbursements_data,
        'message': "Reimbursements fetched successfully!"
    }), 200
    
# Fetch All Reimbursements in Descending Order
@reimbursement_blueprint.route('/get/all-users/reimbursement/list', methods=['GET'])
@jwt_required()
def get_all_reimbursements():
    reimbursements = Reimbursement.query.order_by(Reimbursement.created_at.desc()).all()
    reimbursements_data = [reimbursement_to_dict(reimbursement) for reimbursement in reimbursements]
    return jsonify({
        'success': True,
        'status_code': 200,
        'data': reimbursements_data,
        'message': "All reimbursements fetched successfully!"
    }), 200

    
# Function to convert Reimbursement object to dictionary
def reimbursement_to_dict(reimbursement):
    return {
        'id': reimbursement.id,
        'user_id': reimbursement.user_id,
        'email': reimbursement.email,
        'upi_id': reimbursement.upi_id,
        'expense_date': reimbursement.expense_date.strftime("%Y-%m-%d"),
        'expense_item': reimbursement.expense_item,
        'expense_cost': reimbursement.expense_cost,
        'quantity': reimbursement.quantity,
        'sum': reimbursement.sum,
        'receipt': reimbursement.receipt,
        'total_amt': reimbursement.total_amt,
        'ref_no': reimbursement.ref_no,
        'status': reimbursement.status,
        'label': reimbursement.label,
        'created_at': reimbursement.created_at,
        'updated_at': reimbursement.updated_at
    }
