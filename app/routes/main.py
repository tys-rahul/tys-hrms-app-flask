from flask import Blueprint
from app.resources.auth import auth_blueprint
from app.resources.roles import roles_blueprint
from app.resources.admin import admin_blueprint
from app.resources.professional import professional_blueprint
from app.resources.personal import personal_blueprint
from app.resources.education import education_blueprint
from app.resources.bank import bank_blueprint
from app.resources.family import family_blueprint
from app.resources.office_location import OfficeLocation_blueprint
from app.resources.project import project_blueprint
from app.resources.attendance import attendance_blueprint
from app.resources.experience_details import experience_blueprint
from app.resources.regularizations import regularization_blueprint
from app.resources.holidays import holidays_blueprint
from app.resources.leaves import leaves_blueprint
from app.resources.reimbursement import reimbursement_blueprint
from app.resources.notification import notification_blueprint

main_blueprint = Blueprint('main', __name__)
auth_blueprints = [
    auth_blueprint,
    roles_blueprint,
    professional_blueprint,
    personal_blueprint,
    education_blueprint,
    bank_blueprint,
    family_blueprint,
    OfficeLocation_blueprint,
    project_blueprint,
    attendance_blueprint,
    experience_blueprint,
    regularization_blueprint,
    holidays_blueprint,
    leaves_blueprint,
    reimbursement_blueprint,
    notification_blueprint,
]

for bp in auth_blueprints:
    main_blueprint.register_blueprint(bp, url_prefix='/auth')

main_blueprint.register_blueprint(admin_blueprint, url_prefix='/admin')

