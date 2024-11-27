from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import jwt_required
from app.utils.decorators import permission_required
from datetime import datetime, timedelta
from sqlalchemy import and_
from app.models.attendance import Attendance
from app.models.regularization import Regularization
from app.models.leaves import Leave
from app.models.reimbursement import Reimbursement
from app.models.professional import Professional
from app.models.personal import Personal
from app.models.holidays import Holidays
import calendar
from dateutil import parser
from sqlalchemy.exc import SQLAlchemyError

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/update/user-status/<int:user_id>', methods=['PUT'])
@jwt_required()
# @permission_required('update_user_status')  
def update_user_status(user_id):
    data = request.get_json()
    status = data.get('status')

    if status not in [0, 1]:
        return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Status must be either 0 or 1"
            }), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "User not found"
            }), 404

    user.status = status
    db.session.commit()

    if status == 0:
        return jsonify({
                'success': True,
                'status_code': 200,
                'data': [],
                'message': "User activated successfully!"
            }), 200
    else:
        return jsonify({
                'success': True,
                'status_code': 200,
                'data': [],
                'message': "User deactivated successfully!"
            }), 200

@admin_blueprint.route('/get/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [{"id": user.id, 'username': user.username, "email": user.email, "contact_no": user.contact_no, "status": user.status, "user_type": user.user_type, "work_location_type": user.work_location_type} for user in users],
                'message': "Data fetched successfully!"
            }), 200


@admin_blueprint.route('/delete/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
# @permission_required('Admin')
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': ERROR_USER_NOT_FOUND
            }), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({
                'success': True,
                'status_code': 200,
                'data': [],
                'message': SUCCESS_USER_DELETED
            }), 200
    


@admin_blueprint.route('/get/attendance/monthly/overview', methods=['GET'])
@jwt_required()
def attendance_details():
    try:
        user_counts = []

        # Ensure month and year query parameters are provided
        month_param = request.args.get('month')
        year_param = request.args.get('year')

        if not month_param or not year_param:
            return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Both 'month' and 'year' query parameters are required."
            }), 400

        # Parse month and year from parameters
        try:
            month = datetime.strptime(month_param, "%B").month
            year = int(year_param)
        except ValueError:
            return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Invalid 'month' or 'year' format. Provide month as full name (e.g., October) and year as a number."
            }), 400

        month_name = calendar.month_name[month]

        # Calculate working days
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, calendar.monthrange(year, month)[1])
        working_days = [
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)
            if (start_date + timedelta(days=i)).weekday() < 5 or
               ((start_date + timedelta(days=i)).weekday() == 5 and (start_date + timedelta(days=i)).day % 2 != 0)
        ]
        holiday_count = Holidays.query.filter_by(year=year, month=month_name).count()
        total_working_days = len(working_days) - holiday_count

        # Query user data
        users = User.query.filter(and_(User.status == '0', User.user_type != 'admin')).all()
        six_months_ago = datetime.now() - timedelta(days=6 * 30)

        for user in users:
            attendance = Attendance.query.filter_by(user_id=user.id, attendance_year=year, attendance_month=month_name).all()
            attendance_counts = {
                "Present": Attendance.query.filter_by(user_id=user.id, attendance_year=year, attendance_month=month_name, attendance_status='Present').count(),
                "Late": Attendance.query.filter_by(user_id=user.id, attendance_year=year, attendance_month=month_name, attendance_status='Late').count(),
                "Halfday": Attendance.query.filter_by(user_id=user.id, attendance_year=year, attendance_month=month_name, attendance_status='Halfday').count(),
                "Absent": Attendance.query.filter_by(user_id=user.id, attendance_year=year, attendance_month=month_name, attendance_status='Absent').count(),
                "Leave": Attendance.query.filter_by(user_id=user.id, attendance_year=year, attendance_month=month_name, attendance_status='Leave').count(),
            }
            user_profile_pic = Personal.query.filter_by(user_id=user.id).first()
            professional = Professional.query.filter_by(user_id=user.id).first()

            # Calculate total worked hours
            total_hours = [att.total_hours for att in attendance]
            total_seconds = 0

            for time in total_hours:
                time = time.strip()  

                if time and ':' in time:
                    time_parts = time.split(':')

                    if len(time_parts) == 2:  
                        try:
                            h, m = time_parts
                            total_seconds += int(h) * 3600 + int(m) * 60
                        except ValueError:
                            continue
                    else:
                        continue
                else:
                    continue

            worked_hours = f"{total_seconds // 3600}:{(total_seconds % 3600) // 60}"

            if professional and professional.joining_date:
                try:
                    joining_date = datetime.strptime(professional.joining_date, "%Y-%m-%d")  
                except ValueError:
                    joining_date = None
            else:
                joining_date = None

            isVerified = joining_date and joining_date <= six_months_ago if joining_date else False
    
            user_data = {
                "presentCount": attendance_counts["Present"],
                "lateCount": attendance_counts["Late"],
                "halfdayCount": attendance_counts["Halfday"],
                "absenceCount": attendance_counts["Absent"],
                "leaveCount": attendance_counts["Leave"],
                "fullName": f"{user.username}",
                "email": user.email,
                "pic": user_profile_pic.src if user_profile_pic else "default.jpg",
                "pro": {
                    "designation": professional.designation if professional else "N/A",
                    "experience": professional.experience if professional else "N/A",
                },
                "isVerified": isVerified,
                "workedInMonth": worked_hours,
                "totalWorkHourInMonth": total_working_days * 9,
            }
            user_counts.append(user_data)

        return jsonify({
            'success': True,
            'status_code': 200,
            'data': {
                'userCounts': user_counts,
                'currentMonth': month_name,
                'currentYear': year,
                'totalWorkingDays': total_working_days
            },
            'message': "Attendance details fetched successfully!"
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'status_code': 500,
            'data': [],
            'message': f"An error occurred: {str(e)}"
        }), 500
        
@admin_blueprint.route('/update/regularization/status', methods=['PUT'])
@jwt_required()
def approve_or_reject_regularization():
    try:
        data = request.get_json()
        att_id = data.get('att_id')  
        action_type = data.get('type')  
        comment = data.get('comment', 'NA')  

        if not att_id or not action_type:
            return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Missing attendance ID or action type"
            }), 400
        
        
        attendance = Attendance.query.filter_by(id=att_id).first()
        if not attendance:
            return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "Attendance record not found"
            }), 404
        
        
        regularization = Regularization.query.filter_by(att_id=att_id).first()
        if not regularization:
            return jsonify({
                'success': False,
                'status_code': 404,
                'data': [],
                'message': "Regularization record not found"
            }), 404
        
        if action_type == "approve":
            regularization.status = "Approved"
            regularization.comment = "Approved"
            attendance.attendance_status = "Present"  
        elif action_type == "reject":
            regularization.status = "Rejected"
            regularization.comment = comment
            attendance.attendance_status = "Absent"  
        else:
            return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Invalid action type. Must be 'approve' or 'reject'"
            }), 400
        
        # Save the changes
        db.session.commit()

        return jsonify({
            'success': True,
            'status_code': 200,
            'data': [],
            'message': f"Regularization {action_type}d successfully"
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'status_code': 500,
            'data': [],
            'message': str(e)
        }), 500
        
@admin_blueprint.route('/update/leave/status', methods=['PUT'])
@jwt_required()
def leave_status_approval():
    data = request.get_json()
    leave_id = data.get('leave_id')
    user_id = data.get('user_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    action_type = data.get('type')  # Changed from 'status' to 'type'
    rejection_reason = data.get('rej_reason', 'NA')

    # Fetch leave record
    leave = Leave.query.filter_by(user_id=user_id, start_date=start_date).first()
     # leave_status = LeaveStatus.query.filter_by(user_id=user_id).first()
     
    if not leave:
        return jsonify({
            'success': False,
            'status_code': 404,
            'data': [],
            'message': "Leave record not found!"
        }), 404

    # if not leave_status:
    #     return jsonify({
    #         'success': False,
    #         'status_code': 404,
    #         'data': [],
    #         'message': "Leave status not found!"
    #     }), 404
    
    if end_date == 'NA':
        # Single-day leave
        if action_type == 'approve':
            leave.status = 'Approved'
            leave.comment = 'NA' 
            # leave_status.bal_leave += 1
            # leave_status.avail_leave += 1
            # leave_status.save()
        elif action_type == 'reject':
            leave.status = 'Rejected'
            leave.comment = rejection_reason
        else:
            return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Invalid action type!"
            }), 400

        # Commit changes to the database
        db.session.commit()

        return jsonify({
            'success': True,
            'status_code': 200,
            'data': [],
            'message': "Leave status updated successfully!"
        }), 200
    else:
        # Multi-day leave
        if action_type == 'approve':
            leave.status = 'Approved'
        elif action_type == 'reject':
            leave.status = 'Rejected'
            leave.comment = rejection_reason

            # Calculate leave days
            start = datetime.strptime(str(leave.start_date), '%Y-%m-%d')
            end = datetime.strptime(str(leave.end_date), '%Y-%m-%d')
            leave_dates = []
            while start <= end:
                if start.weekday() < 5 or (start.weekday() == 5 and start.day % 2 != 0): 
                    leave_dates.append(start.date())
                start += timedelta(days=1)

            num_of_days = len(leave_dates)
            # leave_status.bal_leave += num_of_days
            # leave_status.avail_leave += num_of_days
            # leave_status.save()
            
            # Update leave balance logic can go here

        else:
            return jsonify({
                'success': False,
                'status_code': 400,
                'data': [],
                'message': "Invalid action type!"
            }), 400

        # Commit changes to the database
        db.session.commit()

        return jsonify({
            'success': True,
            'status_code': 200,
            'data': [],
            'message': "Leave status updated successfully!"
        }), 200

@admin_blueprint.route('/update/reimbursement/status', methods=['PUT'])
@jwt_required()
def update_reimbursement_status():
    data = request.get_json()

    # Validate input
    reim_id = data.get('reimId')
    reim_status = data.get('reim_status')
    ref_no = data.get('ref_no', 'NA')

    if not reim_id or reim_status not in [0, 1]:
        return jsonify({
            'success': False,
            'status_code': 400,
            'data': [],
            'message': "Invalid input data!"
        }), 400

    # Fetch the reimbursement record
    reimbursement = Reimbursement.query.filter_by(id=reim_id).first()

    if not reimbursement:
        return jsonify({
            'success': False,
            'status_code': 404,
            'data': [],
            'message': "Reimbursement record not found!"
        }), 404

    # Update the status and ref_no based on reim_status
    if reim_status == 0:  
        reimbursement.status = 'Approved'
        reimbursement.ref_no = ref_no
    else:  
        reimbursement.status = 'Rejected'
        reimbursement.ref_no = 'NA'

    # Save changes
    db.session.commit()

    return jsonify({
        'success': True,
        'status_code': 200,
        'data': {
            'id': reimbursement.id,
            'user_id': reimbursement.user_id,
            'status': reimbursement.status,
            'ref_no': reimbursement.ref_no
        },
        'message': "Reimbursement status updated successfully!"
    }), 200
    
@admin_blueprint.route('/get/attendance/monthly/report', methods=['GET'])
@jwt_required()
def view_user_attendance_monthly_details():
    user_id = request.args.get('user_id')
    year = request.args.get('year')
    month_name = request.args.get('month')

    # Validate input
    if not user_id or not year or not month_name:
        return jsonify({
            'success': False,
            'status_code': 400,
            'data': None,
            'message': 'Missing required parameters.'
        }), 400

    try:
        # Convert month name to a numeric month
        month = datetime.strptime(month_name, "%B").month
    except ValueError:
        return jsonify({
            'success': False,
            'status_code': 400,
            'data': None,
            'message': 'Invalid month name.'
        }), 400

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({
            'success': False,
            'status_code': 404,
            'data': None,
            'message': 'User not found.'
        }), 404

    professional = Professional.query.filter_by(user_id=user_id).first()
    designation = professional.designation if professional else "NA"
    joining_date = parser.parse(professional.joining_date) if professional and professional.joining_date else None
    is_verified = joining_date <= datetime.now() - timedelta(days=180) if joining_date else False

    attendance_records = Attendance.query.filter_by(
        user_id=user_id, attendance_year=year, attendance_month=month_name
    ).order_by(Attendance.id.desc()).all()

    total_seconds = 0
    for record in attendance_records:
        time_parts = record.total_hours.replace("hr", "").replace("min", "").strip().split(":")
        if len(time_parts) == 2:
            hours, minutes = map(int, time_parts)
            total_seconds += hours * 3600 + minutes * 60

    hours_worked = total_seconds // 3600
    minutes_worked = (total_seconds % 3600) // 60
    worked_in_month = f"{hours_worked}:{minutes_worked:02d}"

    start_date = datetime(int(year), month, 1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    total_days = (end_date - start_date).days + 1

    working_days = [
        start_date + timedelta(days=i) for i in range(total_days)
        if (start_date + timedelta(days=i)).weekday() < 5
    ]
    holidays_count = Holidays.query.filter_by(year=int(year), month=month_name).count()
    total_working_days = len(working_days) - holidays_count

    present_count = Attendance.query.filter_by(
        user_id=user_id, attendance_year=year, attendance_month=month_name, attendance_status='Present'
    ).count()
    late_count = Attendance.query.filter_by(
        user_id=user_id, attendance_year=year, attendance_month=month_name, attendance_status='Late'
    ).count()
    halfday_count = Attendance.query.filter_by(
        user_id=user_id, attendance_year=year, attendance_month=month_name, attendance_status='Halfday'
    ).count()
    absent_count = Attendance.query.filter_by(
        user_id=user_id, attendance_year=year, attendance_month=month_name, attendance_status='Absent'
    ).count()
    leave_count = Attendance.query.filter_by(
        user_id=user_id, attendance_year=year, attendance_month=month_name, attendance_status='Leave'
    ).count()

    profile_src = Personal.query.filter_by(user_id=user_id).first()
    src = profile_src.src if profile_src else "NA"

    response = {
        "user": {"id": user.id, "email": user.email},
        "designation": designation,
        "isVerified": is_verified,
        "year": year,
        "month": month_name,
        "workedInMonth": worked_in_month,
        "totalWorkingDays": total_working_days,
        "attendance": {
            "presentCount": present_count,
            "lateCount": late_count,
            "halfdayCount": halfday_count,
            "absentCount": absent_count,
            "leaveCount": leave_count,
        },
        "leaveBalance": "NA",  # Replace with actual logic.
        "profileSrc": src,
    }

    return jsonify({
        'success': True,
        'status_code': 200,
        'data': response,
        'message': 'Monthly attendance report fetched successfully!'
    }), 200
