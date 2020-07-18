from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from flask import abort
from datetime import datetime
import requests
import os
import nanoid
import logging

from ..config import cfg
from ..db import *
from .. import mails


def get_user_info(u_email):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == u_email
        )
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
                'key': key.body,
                'description': key.description,
                'update_time': key.update_time,
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
                'access_issued': access.issued,
            })
    return result


def get_users(status):
    result = []
    with get_session() as s:
        users = s.query(User).filter(
                User.status == status
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
