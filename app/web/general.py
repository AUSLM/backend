from flask import (Blueprint, request, redirect, url_for,
                   render_template, jsonify, abort)
from flask_login import (login_required, login_user, logout_user, current_user)

from ..config import cfg

import logging


bp = Blueprint('general_web', __name__)


@bp.route('/')
@login_required
def home():
    return render_template(
        '/home.html',
        current_user=current_user
    )


@bp.route('/instructions')
@login_required
def instructions():
    return render_template(
        '/instructions.html',
        current_user=current_user
    )
