from flask import abort
import logging

from ..db import *
from .general import save_log


def get_user_info(u_email):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == u_email
        ).one_or_none()
        if not user:
            abort(404, 'No user with this id')

        return {
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "service_status": user.service_status
        }


def get_user_keys(u_email):
    result = []
    with get_session() as s:
        keys = s.query(User, PublicKey).filter(
                User.email == u_email,
                User.status == 'active',
                PublicKey.u_id == User.id,
                PublicKey.status == 'active'
        ).all()
        for _, key in keys:
            result.append({
                'id': key.id,
                'key': key.key,
                'name': key.name,
                'upload_time': key.upload_time.isoformat(timespec='minutes', sep=' '),
            })
    return result


def get_user_machines(u_email):
    result = []
    with get_session() as s:
        user_machines = s.query(User, Access, Machine).filter(
                User.id == Access.u_id,
                Access.m_id == Machine.id,
                User.email == u_email,
                Access.status == 'active',
                Machine.status == 'active'
        ).all()
        for _, access, machine in user_machines:
            result.append({
                'id': machine.id,
                'address': machine.address,
                'domain': machine.domain,
                'os': machine.operating_system,
                'os_version': machine.os_version,
                'access_issued': access.issued.isoformat(timespec='minutes', sep=' '),
            })
    return result


def get_users(status):
    result = []
    with get_session() as s:
        users = s.query(User).filter(
                User.status == status,
                User.service_status == 'user'
        ).all()
        for user in users:
            result.append({
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'surname': user.surname,
                'service_status': user.service_status,
            })
    return result
