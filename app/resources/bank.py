from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.bank import Bank
from flask_jwt_extended import jwt_required

bank_blueprint = Blueprint('bank_blueprint', __name__)

@bank_blueprint.route('/get/all-users/bank/list', methods=['GET'])
@jwt_required()
def get_banks():
    banks = Bank.query.all()
    return jsonify([bank.to_dict() for bank in banks]), 200

@bank_blueprint.route('/get/user/bank-details/<int:id>', methods=['GET'])
@jwt_required()
def get_bank(id):
    bank = Bank.query.get_or_404(id)
    return jsonify(bank.to_dict()), 200

@bank_blueprint.route('/add/user/bank-details', methods=['POST'])
@jwt_required()
def create_bank():
    data = request.get_json()
    new_bank = Bank(**data)
    db.session.add(new_bank)
    db.session.commit()
    return jsonify(new_bank.to_dict()), 201

@bank_blueprint.route('/update/user/bank-details/<int:id>', methods=['PUT'])
@jwt_required()
def update_bank(id):
    bank = Bank.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(bank, key, value)
    db.session.commit()
    return jsonify(bank.to_dict()), 200

@bank_blueprint.route('/delete/user/bank-details/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_bank(id):
    bank = Bank.query.get_or_404(id)
    db.session.delete(bank)
    db.session.commit()
    return '', 204

def to_dict(self):
    return {
        "id": self.id,
        "bank_name": self.bank_name,
        "account_no": self.account_no,
        "ifsc_code": self.ifsc_code,
        "branch_name": self.branch_name,
        "bank_address": self.bank_address,
        "pan_card": self.pan_card,
        "aadhar_card": self.aadhar_card,
        "aadhar_img": self.aadhar_img,
        "pan_img": self.pan_img,
        "bank_passbook_img": self.bank_passbook_img,
        "label": self.label,
        "status": self.status,
        "user_id": self.user_id,
    }

Bank.to_dict = to_dict
