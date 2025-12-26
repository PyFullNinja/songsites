from flask import request
from .models import db, Logs

def new_log(description):
    log =  Logs(
        description=description,
        ip=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(log)
    db.session.commit()