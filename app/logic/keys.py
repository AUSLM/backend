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
from .general import save_log


def upload_public_key(u_id, key, name):
    with get_session() as s:
        user = s.query(User).get(u_id)
        if not user:
            abort(404, "User not found.")

        public_key = s.query(PublicKey).filter(
                PublicKey.key == key
        ).one_or_none()

        if public_key:
            if public_key.status == 'banned':
                abort(409, "Can't add banned key")
            public_key.status = 'active'
            public_key.name = name
            public_key.upload_time = datetime.utcnow()
        else:
            new_public_key = PublicKey(u_id=u_id, key=key, name=name)
            s.add(new_public_key)

        s = save_log(s, user.email, 'uploaded new ssh-key','')
        logging.info(f'Uploading new public key for user [{user.email}]')


def delete_public_key(e_email, u_email, k_id):
    with get_session() as s:
        public_key = s.query(PublicKey).filter(
                PublicKey.id == k_id,
                PublicKey.status == 'active'
        ).one_or_none()
        if not public_key:
            abort(404, 'Key not found.')

        exec_user = s.query(User).filter(
                User.email == e_email
        ).one_or_none()

        if exec_user.service_status != 'user' and e_email != u_email:
            public_key.status = 'banned'

            s = save_log(s, e_email, 'banned ssh-key',f'of {u_email}')
            logging.info(f'Banning public key for user [{u_email}]')
        elif exec_user.service_status == 'user' and e_email != u_email:
            abort(404, 'Key not found.')
        else:
            public_key.status = 'deleted'

            s = save_log(s, u_email, 'deleted ssh-key','')
            logging.info(f'Deleting public key for user [{u_email}]')


def key_info(e_email, u_email, k_id):
    with get_session() as s:
        public_key = s.query(PublicKey).filter(
                PublicKey.id == k_id,
                PublicKey.status == 'active'
        ).one_or_none()

        if not public_key:
            abort(404, 'Key not found.')

        exec_user = s.query(User).filter(
                User.email == e_email
        ).one_or_none()
            
        if exec_user.service_status == 'user' and e_email != u_email:
            abort(404, 'Key not found.')
        else:
            return {
                'key': public_key.key,
                'name': public_key.name,
                'upload_time': public_key.upload_time.isoformat(timespec='minutes', sep=' ')
            }
