from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_
from flask import abort
from datetime import datetime
import requests
import os
import nanoid
import logging

from ..config import cfg
from ..db import *
from .. import mails


def grant_access(e_email, u_emails, addrs):
    with get_session() as s:
        user = s.query(User).filter(
                User.email.in_(u_emails)
        )
        machines = s.query(Machine).filter(
                Machine.address.in_(addrs),
                Machine.status == 'active'
        )
        users_string = ''
        machines_string = ''
        for user in users:
            users_string = users_string + user.login + ' '
            machines_string = ''
            for machine in machines:
                machines_string += f"{machine.domain} ({machine.address}) "
                access = s.query(Access).filter(
                        Access.u_id == user.id,
                        Access.m_id == machine.id,
                        Access.status == 'active'
                ).one_or_none()
                if access:
                    if access.status == 'deleted':
                        access.status == 'active'
                else:
                    access = Access(u_id=user.id, m_id=machine.id)
                    s.add(access)
        return [users_string, machines_string]


def revoke_access(e_email, u_emails, addrs):
    with get_session() as s:
        user = s.query(User).filter(
                User.email.in_(u_emails)
        )
        machines = s.query(Machine).filter(
                Machine.address.in_(addrs),
                Machine.status == 'active'
        )
        users_string = ''
        machines_string = ''
        for user in users:
            users_string += user.login + ' '
            machines_string = ''
            for machine in machines:
                machines_string += f"{machine.domain} ({machine.address}) "
                access = s.query(Access).filter(
                    Access.u_id == user.id,
                    Access.m_id == machine.id,
                    Access.status == 'active'
                ).one_or_none()
                if access:
                    access.status = 'deleted'
                    access.disabled = datetime.utcnow()
        return [users_string, machines_string]
