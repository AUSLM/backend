from flask import (Blueprint, request, redirect, url_for,
                   render_template, jsonify, abort)
from flask_login import (login_required, login_user, logout_user, current_user)

from ..logic import accounts as accounts_logic
from ..config import cfg

import logging


bp = Blueprint('machines_web', __name__)


@bp.route('/managing/machines')
@login_required
def manage_machines():
    return render_template(
        '/manage_machines.html',
        current_user=current_user
    )


@bp.route('/machines')
@login_required
def machines():
    return render_template(
        '/machines.html',
        current_user=current_user
    )
