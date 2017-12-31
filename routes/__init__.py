from flask import session,redirect,url_for

from models.user import User
from utils import log

def current_user():
    uid = session.get('user_id', -1)
    log('current_user的id ->',uid)
    u = User.find_by(id=int(uid))
    log('current_user ->', u)
    return u
