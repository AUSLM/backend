from flask import Blueprint
from flask_login import (login_required, current_user)

from . import *
from ..auth import admin_route
from ..logic import accesses as accesses_logic
from ..validation.validation import validate
from ..validation import schemas


bp = Blueprint('accesses_api_web', __name__)


@bp.route('/grant_access', methods=['POST'])
@login_required
@admin_route
def grant_access():
    data = validate(get_json(), schemas.grant_access)
    accesses_logic.grant_access(current_user.email, data['email'], data['address'])
    return make_ok(200, "Access was granted")


@bp.route('/revoke_access', methods=['POST'])
@login_required
@admin_route
def revoke_access():
    data = validate(get_json(), schemas.revoke_access)
    accesses_logic.revoke_access(current_user.email, data['email'], data['address'])
    return make_ok(200, "Access was revoked")
