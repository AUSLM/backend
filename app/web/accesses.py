from flask import (Blueprint, request, redirect, url_for,
                   render_template, jsonify, abort)
from flask_login import (login_required, login_user, logout_user, current_user)

from ..logic import accesses as accesses_logic
from ..config import cfg

import logging


bp = Blueprint('accesses_web', __name__)


@bp.route('/management/accesses')
@login_required
def manage_accesses():
    if current_user.service_status == 'user':
        abort(404, "No rights")
    return render_template(
        '/manage_accesses.html',
        current_user=current_user
    )
