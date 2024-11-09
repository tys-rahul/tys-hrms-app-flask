from flask import Blueprint, request, jsonify
from app.models.holidays import Holidays
from app.extensions import db
from datetime import datetime, timezone
from flask_jwt_extended import jwt_required

holidays_blueprint = Blueprint('holidays', __name__)

@holidays_blueprint.route('/add/holiday', methods=['POST'])
@jwt_required()
def create_holiday():
    data = request.json
    try:
        holiday_date = datetime.strptime(data.get('holiday_date'), '%Y-%m-%d') if data.get('holiday_date') else None
        holiday_name = data.get('holiday_name', 'NA')
        month = data.get('month')
        year = data.get('year')
        
        new_holiday = Holidays(
            holiday_date=holiday_date,
            holiday_name=holiday_name,
            month=month,
            year=year
        )
        
        db.session.add(new_holiday)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'status_code': 201,
            'data': holiday_to_dict(new_holiday),
            'message': "Holiday created successfully!"
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'status_code': 400,
            'error': str(e),
            'message': "An error occurred while creating the holiday."
        }), 400

@holidays_blueprint.route('/holidays/<int:id>', methods=['GET'])
@jwt_required()
def get_holiday(id):
    holiday = Holidays.query.get(id)
    if holiday:
        return jsonify({
            'success': True,
            'status_code': 200,
            'data': holiday_to_dict(holiday),
            'message': "Holiday fetched successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'error': "Holiday not found",
        'message': "Holiday not found"
    }), 404

@holidays_blueprint.route('/get/holiday/list', methods=['GET'])
@jwt_required()
def get_all_holidays():
    holidays = Holidays.query.all()
    return jsonify({
        'success': True,
        'status_code': 200,
        'data': [holiday_to_dict(holiday) for holiday in holidays],
        'message': "Data fetched successfully!"
    }), 200

@holidays_blueprint.route('/update/holiday/<int:id>', methods=['PUT'])
@jwt_required()
def update_holiday(id):
    data = request.json
    holiday = Holidays.query.get(id)
    if holiday:
        holiday.holiday_date = datetime.strptime(data.get('holiday_date'), '%Y-%m-%d') if data.get('holiday_date') else holiday.holiday_date
        holiday.holiday_name = data.get('holiday_name', holiday.holiday_name)
        holiday.month = data.get('month', holiday.month)
        holiday.year = data.get('year', holiday.year)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'status_code': 200,
            'data': holiday_to_dict(holiday),
            'message': "Holiday updated successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'error': "Holiday not found",
        'message': "Holiday not found"
    }), 404

@holidays_blueprint.route('/delete/holiday/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_holiday(id):
    holiday = Holidays.query.get(id)
    if holiday:
        db.session.delete(holiday)
        db.session.commit()
        return jsonify({
            'success': True,
            'status_code': 200,
            'message': "Holiday deleted successfully!"
        }), 200
    return jsonify({
        'success': False,
        'status_code': 404,
        'error': "Holiday not found",
        'message': "Holiday not found"
    }), 404


def holiday_to_dict(holiday):
    return {
        "id": holiday.id,
        "holiday_date": holiday.holiday_date.strftime('%Y-%m-%d') if holiday.holiday_date else None,
        "holiday_name": holiday.holiday_name,
        "month": holiday.month,
        "year": holiday.year,
        "created_at": holiday.created_at.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": holiday.updated_at.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    }
