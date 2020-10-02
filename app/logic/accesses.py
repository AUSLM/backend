from flask import abort
from datetime import datetime
import logging

from ..db import *
from .general import save_log


def grant_access(e_email, u_email, addr):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == u_email,
                User.status == 'active'
        ).one_or_none()
        machine = s.query(Machine).filter(
                Machine.address == addr,
                Machine.status == 'active'
        ).one_or_none()

        if not user:
            abort(404, 'User not found')
        if not machine:
            abort(404, 'Machine not found')

        access = s.query(Access).filter(
                Access.u_id == user.id,
                Access.m_id == machine.id,
        ).one_or_none()

        if access:
            if access.status == 'deleted':
                access.status = 'active'
                access.issued = datetime.utcnow()
        else:
            access = Access(u_id=user.id, m_id=machine.id)
            s.add(access)

        s = save_log(s, e_email, 'grant access', f'to {u_email} to {addr}')
        logging.info(f'Grant [{u_email}] to [{addr}]')


def revoke_access(e_email, u_email, addr):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == u_email,
                User.status == 'active'
        ).one_or_none()
        machine = s.query(Machine).filter(
                Machine.address == addr,
                Machine.status == 'active'
        ).one_or_none()

        if not user:
            abort(404, 'User not found')
        if not machine:
            abort(404, 'Machine not found')
        if user.service_status != 'user':
            abort(409, "Can't revoke access from admins!")

        access = s.query(Access).filter(
                Access.u_id == user.id,
                Access.m_id == machine.id,
                Access.status == 'active'
        ).one_or_none()

        if access:
            access.status = 'deleted'
            access.disabled = datetime.utcnow()

        s = save_log(s, e_email, 'revoke access', f'from {u_email} from {addr}')
        logging.info(f'Revoke [{u_email}] from [{addr}]')
