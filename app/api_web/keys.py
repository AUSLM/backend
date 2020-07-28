from flask import Blueprint, jsonify, request, abort
from flask_login import (login_required, login_user, logout_user, current_user)

from . import *
from ..logic import keys as keys_logic
from ..validation.validation import validate
from ..validation import schemas


bp = Blueprint('keys_api_web', __name__)


@bp.route('/add_key', methods=['POST'])
@login_required
def add_machine():
    data = validate(get_json(), schemas.add_key)
    keys_logic.upload_public_key(current_user.id, data['key'], data['name'])
    return make_ok(201, "Key was added")


@bp.route('/remove_key', methods=['POST'])
@login_required
def remove_key():
    data = validate(get_json(), schemas.remove_key)
    keys_logic.delete_public_key(current_user.email, data['u_email'], data['k_id'])
    return make_ok(200, "Key was removed")


@bp.route('/key_info', methods=['POST'])
@login_required
def key_info():
    data = validate(get_json(), schemas.remove_key)
    return keys_logic.key_info(current_user.email, data['u_email'], data['k_id'])
