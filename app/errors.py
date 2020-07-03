from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from flask import jsonify, abort, request

from .api import *
from .web import *


def add_error_handlers(app):
    app.register_error_handler(401, unauthorized_handler)
    app.register_error_handler(404, not_found_handler)
    app.register_error_handler(405, make_405)
    app.register_error_handler(500, server_error_handler)

    app.register_error_handler(HTTPException, http_error_handler)

    # legacy
    # app.register_error_handler(IntegrityError, make_400)
    # app.register_error_handler(KeyError, make_400)
    # app.register_error_handler(AttributeError, make_400)
    # app.register_error_handler(ValueError, make_422)
    # app.register_error_handler(IndexError, make_422)


def http_error_handler(e):
    return jsonify(error=e.description), e.code


def on_json_loading_failed(err, e):
    abort(415, 'Expected json')


def unauthorized_handler(e):
    if request.path.startswith('/api/'):
        return make_401(e)
    else:
        return web_401(e)


def not_found_handler(e):
    if request.path.startswith('/api/'):
        if request.path.startswith('/api/edu/') and request.path.endswith('delete'):
            return make_404(e, "ENF")
        else:
            return make_404(e, "NF")
    else:
        if request.path.startswith('/event/'):
            return web_404(e, "ENF")
        else:
            return web_404(e, "NF")


def server_error_handler(e):
    if request.path.startswith('/api/'):
        return server_500_error(e)
    else:
        return web_500(e)
