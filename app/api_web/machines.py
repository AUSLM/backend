from flask import Blueprint
from flask_login import login_required, current_user

from . import *
from ..logic import machines as machines_logic
from ..validation.validation import validate
from ..validation import schemas


bp = Blueprint('machines_api_web', __name__)


@bp.route('/add_machine', methods=['POST'])
@login_required
def add_machine():
    if current_user.service_status not in ['superadmin', 'admin']:
        return api_4xx(404, 'Unknown route')
    data = validate(get_json(), schemas.add_machine)
    machines_logic.add_machine(current_user.email, data['address'], data['domain'])
    return api_ok(201, "Machine was added")


@bp.route('/remove_machine', methods=['POST'])
@login_required
def remove_machine():
    if current_user.service_status not in ['superadmin', 'admin']:
        return api_4xx(404, 'Unknown route')
    data = validate(get_json(), schemas.address)
    machines_logic.remove_machine(current_user.email, data['address'])
    return api_ok(200, "Machine was removed")


@bp.route('/web_terminal', methods=['POST'])
@login_required
def web_terminal():
    data = validate(get_json(), schemas.address)
    return machines_logic.web_terminal(current_user.email, data['address'])
