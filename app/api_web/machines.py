from flask import Blueprint, jsonify, request, abort
from flask_login import (login_required, login_user, logout_user, current_user)

from . import *
from ..logic import machines as machines_logic
from ..auth import pre_login
from ..validation.validation import validate
from ..validation import schemas


bp = Blueprint('machines_api_web', __name__)


@bp.route('/add_machine', methods=['POST'])
@login_required
def add_machine():
    if current_user.service_status not in ['superadmin', 'admin']:
        return make_4xx(403, "No rights")
    data = validate(get_json(), schemas.add_machine)
    machines_logic.add_machine(current_user.email, data['address'], data['domain'])
    return make_ok(201, "Machine was added")


@bp.route('/remove_machine', methods=['POST'])
@login_required
def remove_machine():
    if current_user.service_status not in ['superadmin', 'admin']:
        return make_4xx(403, "No rights")
    data = validate(get_json(), schemas.remove_machine)
    machines_logic.remove_machine(current_user.email, data['address'])
    return make_ok(200, "Machine was removed")
