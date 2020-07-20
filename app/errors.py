from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from flask import jsonify, abort, request

from .api_web import *
from .web import *


def add_error_handlers(app):
    app.register_error_handler(401, unauthorized_handler)
    app.register_error_handler(404, not_found_handler)
    app.register_error_handler(405, make_405)
    app.register_error_handler(500, server_error_handler)

    app.register_error_handler(HTTPException, http_error_handler)


def http_error_handler(e):
    return jsonify(error=e.description), e.code


def on_json_loading_failed(err, e):
    abort(415, 'Expected json')


def unauthorized_handler(e):
    if request.path.startswith('/api/'):
        return make_4xx(401, 'Unauthorized')
    else:
        return web_401(e)


def not_found_handler(e):
    if request.path.startswith('/api/'):
        return make_404(e)
    else:
        if request.path.startswith('/user/'):
            return web_404(e, "User")
        elif request.path.startswith('/machine/'):
            return web_404(e, "Machine")
        else:
            return web_404(e, "Page")


def server_error_handler(e):
    if request.path.startswith('/api/'):
        return server_500_error(e)
    else:
        return web_500(e)
