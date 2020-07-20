from flask import Blueprint, jsonify, request, abort
from flask_login import (login_required, login_user, logout_user, current_user)

from . import *
from ..logic import accesses as accesses_logic
from ..validation.validation import validate
from ..validation import schemas


bp = Blueprint('accesses_api_web', __name__)


@bp.route('/grant_access', methods=['POST'])
@login_required
def grant_access():
    if current_user.service_status not in ['superadmin', 'admin']:
        return make_4xx(404, 'Unknown route')
    data = validate(get_json(), schemas.grant_access)
    accesses_logic.grant_access(current_user.email, data['email'], data['address'])
    return make_ok(200, "Access was granted")


@bp.route('/revoke_access', methods=['POST'])
@login_required
def revoke_access():
    if current_user.service_status not in ['superadmin', 'admin']:
        return make_4xx(404, 'Unknown route')
    data = validate(get_json(), schemas.revoke_access)
    accesses_logic.revoke_access(current_user.email, data['email'], data['address'])
    return make_ok(200, "Access was revoked")
