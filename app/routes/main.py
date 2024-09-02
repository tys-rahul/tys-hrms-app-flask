from flask import Blueprint
from app.resources.auth import auth_blueprint
from app.resources.roles import roles_blueprint
from app.resources.admin import admin_blueprint

main_blueprint = Blueprint('main', __name__)
main_blueprint.register_blueprint(auth_blueprint, url_prefix='/auth')
main_blueprint.register_blueprint(roles_blueprint, url_prefix='/auth')
main_blueprint.register_blueprint(admin_blueprint, url_prefix='/admin')

