from flask import Flask, request, jsonify, Blueprint
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func , desc
from app.models.attendance import Attendance
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import pytz

attendance_blueprint = Blueprint('attendance', __name__)

@attendance_blueprint.route('/add/user/attendance', methods=['POST'])
@jwt_required()
def create_attendance():
    try:
        # Getting authenticated user info
        user_info = get_jwt_identity()
        user_id = user_info['user_id']
        email = user_info['email']
        
        # Fetching the user record based on user_id
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({
                'success': False,
                'status_code': 404,
                'message': 'User not found.'
            }), 404

        # Check if the user is active (status is 0)
        if int(user.status) != 0:
            return jsonify({
                'success': False,
                'status_code': 403,
                'message': 'User is not active. Attendance cannot be created.'
            }), 403

        # Get current date and time in IST
        ist_timezone = pytz.timezone("Asia/Kolkata")
        curr_datetime = datetime.now(ist_timezone)
        curr_date = curr_datetime.date()
        curr_time = curr_datetime.time() 

        curr_year = curr_date.year
        curr_month = curr_date.strftime('%B')
        curr_day = curr_date.strftime('%A')
        curr_dateymd = curr_date.strftime('%Y-%m-%d')
        office_time = datetime.strptime('09:30:00', '%H:%M:%S').time()

        # Check if attendance already exists for the current day
        existing_attendance = Attendance.query.filter_by(user_id=user_id, attendance_date=curr_dateymd).first()

        if not existing_attendance:
            # Validate request
            if not request.json.get('coordinate') or not request.json.get('current_address'):
                return jsonify({
                    'success': False,
                    'status_code': 400,
                    'message': 'Coordinate and Current Address are required.'
                }), 400

            # Create new Attendance object
            attendance = Attendance(
                user_id=user_id,
                email=email,
                coordinate=request.json.get('coordinate'),
                current_address=request.json.get('current_address'),
                attendance_year=curr_year,
                attendance_month=curr_month,
                attendance_date=curr_date,
                attendance_day=curr_day,
                in_time=curr_time  
            )

            # Check if the user is late
            if curr_time > office_time:
                attendance.attendance_status = 'Late'
                attendance.is_late = True
            else:
                attendance.attendance_status = 'Present'

            db.session.add(attendance)
            db.session.commit()

            return jsonify({
                'success': True,
                'status_code': 201,
                'data': attendance.to_dict(),
                'message': 'Attendance added successfully!'
            }), 201

        # If in-time is already set, update out-time and calculate total hours
        elif existing_attendance.in_time is not None:
            out_time = curr_datetime.time()  
            in_time = existing_attendance.in_time

            # Calculate total seconds worked and convert to hours and minutes
            total_seconds = (datetime.combine(datetime.today(), out_time) - datetime.combine(datetime.today(), in_time)).total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            total_hours_formatted = f"{int(hours)}:{int(minutes):02}"

            # Check the status based on total hours
            if hours >= 5:
                if in_time < office_time:
                    status = 'Present'
                else:
                    status = 'Late'
            else:
                status = 'Halfday'

            # Update attendance record with out_time and total_hours
            existing_attendance.out_time = out_time
            existing_attendance.total_hours = total_hours_formatted
            existing_attendance.attendance_status = status

            db.session.commit()

            return jsonify({
                'success': True,
                'status_code': 201,
                'data': existing_attendance.to_dict(),
                'message': 'Attendance punched successfully!'
            }), 201

        else:
            return jsonify({
                'success': False,
                'status_code': 400,
                'message': 'Invalid operation.'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'status_code': 500,
            'message': str(e)
        }), 500

@attendance_blueprint.route('/get/all-users/attendances-list', methods=['GET'])
@jwt_required()
def get_all_attendances():
    month = request.args.get('month', type=str)  
    year = request.args.get('year', type=int)    

    try:
        attendances = Attendance.query.filter_by(attendance_year=year, attendance_month=month).order_by(desc(Attendance.attendance_date)).all()

        all_user_attendances = [attendance.to_dict() for attendance in attendances]

        for attendance in all_user_attendances:
            attendance['attendance_month'] = str(attendance['attendance_month'])
            attendance['attendance_year'] = str(attendance['attendance_year'])

        return jsonify({
            'success': True,
            'status_code': 200,
            'data': all_user_attendances,
            'message': 'All User Attendances fetched successfully!!'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'status_code': 500,
            'message': str(e)
        }), 500

@attendance_blueprint.route('/get/user/attendance/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_attendances(user_id):
    month = request.args.get('month', type=str)  
    year = request.args.get('year', type=int)    

    try:
        attendances = Attendance.query.filter_by(user_id=user_id, attendance_year=year, attendance_month=month).order_by(desc(Attendance.attendance_date)).all()

        user_attendances = [attendance.to_dict() for attendance in attendances]

        for attendance in user_attendances:
            attendance['attendance_month'] = str(attendance['attendance_month'])
            attendance['attendance_year'] = str(attendance['attendance_year'])

        return jsonify({
            'success': True,
            'status_code': 200,
            'data': user_attendances,
            'message': 'User Attendances fetched successfully!!'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'status_code': 500,
            'message': str(e)
        }), 500

@attendance_blueprint.route('/get/user/todays-attendance', methods=['GET'])
@jwt_required()
def user_current_attendance():
    current_user_id = get_jwt_identity().get('user_id')  
    
    current_date = datetime.now().strftime('%Y-%m-%d')

    get_attendance = Attendance.query.filter_by(user_id=current_user_id, attendance_date=current_date).all()

    if not get_attendance:
        message = 'User Attendance is not yet created!!'
    else:
        message = 'User Attendance fetched successfully!!'

    response = {
        'success': True,
        'status_code': 200,
        'data': [attendance.to_dict() for attendance in get_attendance],  
        'message': message
    }

    return jsonify(response), 200

@attendance_blueprint.route('/delete/user/attendance/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_attendance(id):
    current_user_id = get_jwt_identity()

    # Check if the current user is an admin
    # if not is_admin(current_user_id):
    #     return jsonify({
    #         'success': False,
    #         'status_code': 403,
    #         'message': 'Admin access required.'
    #     }), 403

    # try:
    attendance = Attendance.query.filter_by(id=id).first()

    if not attendance:
        return jsonify({
            'success': False,
            'status_code': 404,
            'message': 'Attendance record not found.'
        }), 404

    db.session.delete(attendance)
    db.session.commit()

    return jsonify({
        'success': True,
        'status_code': 200,
        'message': 'Attendance record deleted successfully.'
    }), 200

    # except Exception as e:
    #     return jsonify({
    #         'success': False,
    #         'status_code': 500,
    #         'message': str(e)
    #     }), 500

# Create attendance record
@attendance_blueprint.route('/admin/add/attendance', methods=['POST'])
@jwt_required()
def add_attendance():
    data = request.get_json()
    
    # Check if a record already exists with the same user_id and attendance_date
    existing_record = Attendance.query.filter_by(
        user_id=data.get('user_id'),
        attendance_date=datetime.strptime(data['attendance_date'], '%Y-%m-%d')
    ).first()
    
    if existing_record:
        return jsonify({
            'success': False,
            'status_code': 400,
            'message': 'Attendance record already exists for this user and date.'
        }), 400

    try:
        attendance = Attendance(
            user_id=data.get('user_id'),
            email=data.get('email'),
            attendance_year=data.get('attendance_year'),
            attendance_month=data.get('attendance_month'),
            attendance_date=datetime.strptime(data['attendance_date'], '%Y-%m-%d') if data.get('attendance_date') else None,
            attendance_day=data.get('attendance_day'),
            attendance_status=data.get('attendance_status'),
            holiday=data.get('holiday'),
            is_applied=data.get('is_applied'),
            in_time=datetime.strptime(data['in_time'], '%H:%M:%S') if data.get('in_time') else None,
            out_time=datetime.strptime(data['out_time'], '%H:%M:%S') if data.get('out_time') else None,
            total_hours=data.get('total_hours'),
            is_late=data.get('is_late'),
            current_address=data.get('current_address'),
            coordinate=data.get('coordinate'),
            comments=data.get('comments'),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'status_code': 201,
            'data': attendance.to_dict(),
            'message': 'Attendance record added successfully!'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'status_code': 400,
            'message': str(e)
        }), 400
# Edit attendance record
@attendance_blueprint.route('/admin/edit/attendance/<int:id>', methods=['PUT'])
@jwt_required()
def edit_attendance(id):
    data = request.get_json()
    attendance = Attendance.query.get(id)
    
    if not attendance:
        return jsonify({
                'success': False,
                'status_code': 404,
                'message': 'Attendance record not found.'
            }), 404

    try:
        attendance.user_id = data.get('user_id', attendance.user_id)
        attendance.email = data.get('email', attendance.email)
        attendance.attendance_year = data.get('attendance_year', attendance.attendance_year)
        attendance.attendance_month = data.get('attendance_month', attendance.attendance_month)
        attendance.attendance_date = datetime.strptime(data['attendance_date'], '%Y-%m-%d') if data.get('attendance_date') else attendance.attendance_date
        attendance.attendance_day = data.get('attendance_day', attendance.attendance_day)
        attendance.attendance_status = data.get('attendance_status', attendance.attendance_status)
        attendance.holiday = data.get('holiday', attendance.holiday)
        attendance.is_applied = data.get('is_applied', attendance.is_applied)
        attendance.in_time = datetime.strptime(data['in_time'], '%H:%M:%S') if data.get('in_time') else attendance.in_time
        attendance.out_time = datetime.strptime(data['out_time'], '%H:%M:%S') if data.get('out_time') else attendance.out_time
        attendance.total_hours = data.get('total_hours', attendance.total_hours)
        attendance.is_late = data.get('is_late', attendance.is_late)
        attendance.current_address = data.get('current_address', attendance.current_address)
        attendance.coordinate = data.get('coordinate', attendance.coordinate)
        attendance.comments = data.get('comments', attendance.comments)
        attendance.updated_at = datetime.now()

        db.session.commit()
        return jsonify({
                'success': True,
                'status_code': 200,
                'data': attendance.to_dict(),
                'message': 'Attendance record updated successfully!'
            }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'status_code': 400,
            'message': str(e)
        }), 400

def to_dict(self):
    return {
        'id': self.id,
        'user_id': self.user_id,
        'email': self.email,
        'attendance_year': self.attendance_year,
        'attendance_month': self.attendance_month,
        'attendance_date': self.attendance_date.strftime('%Y-%m-%d') if self.attendance_date else None,
        'attendance_day': self.attendance_day,
        'attendance_status': self.attendance_status,
        'holiday': self.holiday,
        'is_applied': self.is_applied,
        'in_time': self.in_time.strftime('%H:%M:%S') if self.in_time else None,  # Convert to string
        'out_time': self.out_time.strftime('%H:%M:%S') if self.out_time else None,  # Convert to string
        'total_hours': self.total_hours,
        'is_late': self.is_late,
        'current_address': self.current_address,
        'coordinate': self.coordinate,
        'comments': self.comments,
        'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
    }


        
Attendance.to_dict = to_dict