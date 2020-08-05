import jwt
import time
import ldap3
import bcrypt
from flask import abort

from .config import cfg
from .db import User, Token, get_session


def user_loader(uc_id):
    with get_session() as s:
        return s.query(User).filter(
                User.cookie_id == uc_id
        ).one_or_none()


def ldap_login(email, password):
    server = f"ldap://{cfg.AD_SERVER_ADDR}"

    connection = ldap3.initialize(server)
    connection.set_option(ldap, OPT_REFERRALS, 0)
    connection.protocol_version = 3
    try:
        connection.simple_bind_s(email, password)
        connection.unbind()
        return True
    except Exception as e:
        return False


def pre_login(email, password):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == email
        ).one_or_none()

        if not user:
            abort(404, 'Invalid user')
        if user.status == 'banned':
            abort(409, 'Trying to login banned user')
        if user.status == 'deleted':
            abort(404, 'Invalid user')
        if user.status == 'unconfirmed':
            abort(409, 'Trying to login unconfirmed user')

        if cfg.AD_USE and email != cfg.SUPER_ADMIN_MAIL:
            if not ldap_login(email, password):
                abort(422, 'Invalid password')
        else:
            pw = str(password).encode('utf-8')
            upw = str(user.password).encode('utf-8')
            if not bcrypt.checkpw(pw, upw):
                abort(422, 'Invalid password')
        return user


def header_loader(header):
    try:
        token = jwt.decode(header, 'secret', algorithms=['HS256'])
    except jwt.exceptions.InvalidTokenError:
        return None
    with get_session() as s:
        pair = s.query(User, Token).filter(
                User.id == token['uid'],
                Token.id == token['jti'],
                Token.status == 'active',
        ).one_or_none()
        return pair[0] if pair else None


def get_jwt(token):
    payload = {
        'jti': str(token.id),
        'iat': token.issued,
        'uid': token.u_id,
    }
    t = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
    return t


def get_token(u_id):
    with get_session() as s:
        token = s.query(Token).filter(
                Token.u_id == u_id,
                Token.status == 'active'
        ).one_or_none()
        if not token:
            return None
        return get_jwt(token)


def reissue_token(u_id):
    with get_session() as s:
        old_token = s.query(Token).filter(
                Token.u_id == u_id,
                Token.status == 'active'
        ).one_or_none()
        if old_token:
            old_token.status = 'deleted'
        token = Token()
        token.u_id = u_id
        s.add(token)
        s.flush()
        s.refresh(token)
        return get_jwt(token)
