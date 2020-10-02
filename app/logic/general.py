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


def save_log(session, executor, action, description):
    act = Logs(executor=executor, action=action, description=description)
    session.add(act)
    return session


def get_activity_logs():
    result = []
    with get_session() as s:
        logs = s.query(Logs).order_by(desc(Logs.id)).all()
        for log in logs:
            result.append({
                'executor': log.executor,
                'action': log.action,
                'description': log.description,
                'action_time': log.action_time.isoformat(timespec='seconds', sep=' '),
            })
    return result


def get_controller_logs():
    result = []
    with get_session() as s:
        logs = s.query(ControllerLogs).order_by(desc(ControllerLogs.id)).all()
        for log in logs:
            result.append({
                'description': log.description,
                'action_time': log.action_time.isoformat(timespec='seconds', sep=' '),
            })
    return result
