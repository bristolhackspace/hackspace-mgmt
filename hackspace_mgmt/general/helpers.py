from functools import wraps
from flask import g, session, request, redirect, url_for
from hackspace_mgmt.models import db, Member

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in_member" not in session:
            return redirect(url_for("general.login", next=request.url))

        g.member = db.session.get(Member, session["logged_in_member"])
        return f(*args, **kwargs)
    return decorated_function