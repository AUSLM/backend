from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from flask import abort
import bcrypt
from datetime import datetime
import requests
import os
import nanoid
import uuid
import logging

from ..config import cfg
from ..db import *
from ..auth import ldap_check
from .. import mails


def register_user(email, password, name, surname):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == email
        ).one_or_none()

        confirmation_link = ''
        while True:
            confirmation_link = nanoid.generate(size=50)
            exists = s.query(User).filter(
                    User.confirmation_link == confirmation_link
            ).one_or_none()
            if not exists:
                break

        if user:
            if user.status == 'deleted':
                user.name = name
                user.surname = surname
                user.status = cfg.DEFAULT_USER_STATUS
                user.confirmation_link = confirmation_link
                if cfg.AD_USE:
                    if not ldap_check(email, password):
                        abort(409, "Can't register via AD because wrong auth")
                    user.password = '-'
                else:
                    pw = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    user.password = pw
            elif user.status == 'banned':
                abort(409, 'User with this email was banned')
            else:
                abort(409, 'Trying to register existing user')
        else:
            user = User(email=email, password='-', name=name, surname=surname,
                        confirmation_link=confirmation_link)

            if cfg.AD_USE:
                if not ldap_check(email, password):
                    abort(409, "Can't register via AD because wrong auth")
            else:
                pw = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user.password = pw
            s.add(user)

        if cfg.DEFAULT_USER_STATUS == 'unconfirmed':
            mails.send_confirm_email(email, confirmation_link)
        logging.info('Registering new user [{}]'.format(email))


def confirm_user(confirmation_link):
    with get_session() as s:
        user = s.query(User).filter(
                User.confirmation_link == confirmation_link
        ).one_or_none()
        if not user:
            abort(404, 'No user with this confirmation link')
        if user.status != 'unconfirmed':
            abort(409, "User is currently confirmed by this link or can't be confirmed")
        user.status = 'active'
        logging.info('User [{}] is confirmed'.format(user.email))


def reset_password(email):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == email,
                User.status == 'active',
        ).one_or_none()
        
        if not user:
            abort(404, 'Invalid user')
        
        new_password = nanoid.generate(size=20)
        npw = bcrypt.hashpw(str(new_password).encode('utf-8'), bcrypt.gensalt())
        user.password = npw.decode('utf-8')
        user.cookie_id = uuid.uuid4()
        mails.send_reset_email(email, new_password)


def change_password(u_id, old_password, new_password):
    if old_password == new_password:
        abort(409, 'Old and new passwords are equal')
    with get_session() as s:
        user = s.query(User).get(u_id)

        opw = str(old_password).encode('utf-8')
        npw = str(new_password).encode('utf-8')
        pw = str(user.password).encode('utf-8')

        if not bcrypt.checkpw(opw, pw):
            abort(422, 'Invalid password')
        npw = bcrypt.hashpw(npw, bcrypt.gensalt())
        user.password = npw.decode('utf-8')
        user.cookie_id = uuid.uuid4()
        return user


def close_all_sessions(u_id, password):
    with get_session() as s:
        user = s.query(User).get(u_id)

        if cfg.AD_USE:
            if not ldap_check(email, password):
                abort(422, 'Invalid password')
        else:
            opw = str(password).encode('utf-8')
            pw = str(user.password).encode('utf-8')
            if not bcrypt.checkpw(opw, pw):
                abort(422, 'Invalid password')
        user.cookie_id = uuid.uuid4()
        return user


# for admins

def change_privileges(u_email, role):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == u_email,
                User.status == 'active',
        ).one_or_none()

        if not user:
            abort(404, 'No user with this email')
        if user.service_status == 'superadmin':
            abort(409, "Can't change superadmin privileges!")
        if user.service_status == role:
            abort(409, 'User already has that role')
        user.service_status = role

        machines = s.query(Machine).filter(
                Machine.status == 'active'
        ).all()

        for machine in machines:
            access = s.query(Access).filter(
                    Access.u_id == user.id,
                    Access.m_id == machine.id,
            ).one_or_none()

            if access:
                if access.status == 'deleted':
                    access.status == 'active'
            else:
                access = Access(u_id=user.id, m_id=machine.id)
                s.add(access)
