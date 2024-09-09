from flask import Flask, request, jsonify, Blueprint
from app.extensions import db
from datetime import datetime
from app.models.office_location import OfficeLocation
from flask_jwt_extended import jwt_required

OfficeLocation_blueprint = Blueprint('OfficeLocation', __name__)

# Get all office locations
@OfficeLocation_blueprint.route('/get/all-office-location/list', methods=['GET'])
@jwt_required()
def get_all_office_locations():
    offices = OfficeLocation.query.all()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [office.to_dict() for office in offices],
                'message': "Data fetched successfully!"
            }), 200

# Get office location details by ID
@OfficeLocation_blueprint.route('/get/office/location/<int:id>', methods=['GET'])
@jwt_required()
def get_office_location(id):
    office = OfficeLocation.query.get(id)
    if not office:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "Office location not found"
            }), 404
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [office.to_dict()],
                'message': "Data fetched successfully!"
            }), 200


# Create a new office location
@OfficeLocation_blueprint.route('/add/office/location', methods=['POST'])
@jwt_required()
def create_office_location():
    data = request.get_json()
    new_office = OfficeLocation(**data)
    db.session.add(new_office)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 201,
                'data': [new_office.to_dict()],
                'message': "Data created successfully!"
            }), 201


# Update office location details
@OfficeLocation_blueprint.route('/update/office/location/<int:id>', methods=['PUT'])
@jwt_required()
def update_office_location(id):
    office = OfficeLocation.query.get(id)
    if not office:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "Office location not found"
            }), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(office, key, value)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [office.to_dict()],
                'message': "Data updated successfully!"
            }), 200

# Delete office location entry
@OfficeLocation_blueprint.route('/delete/office/location/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_office_location(id):
    office = OfficeLocation.query.get(id)
    if not office:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "Office location not found"
            }), 404

    db.session.delete(office)
    db.session.commit()

    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [],
                'message': "Office location deleted successfully!"
            }), 200



def to_dict(self):
        return {
            'id': self.id,
            'office_location': self.office_location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

OfficeLocation.to_dict = to_dict