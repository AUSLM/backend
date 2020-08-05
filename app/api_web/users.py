from flask import Blueprint, jsonify, request, abort
from flask_login import (login_required, login_user, logout_user, current_user)

from . import *
from ..logic import users as users_logic
from ..validation.validation import validate
from ..validation import schemas


bp = Blueprint('users_api_web', __name__)
# TODO ?
