from flask import Blueprint, flash, redirect, render_template, url_for, request, g
from flask_wtf import FlaskForm
from markupsafe import Markup, escape
from wtforms import fields, widgets, ValidationError
from wtforms.validators import InputRequired, NumberRange
from sqlalchemy.dialects.postgresql import insert
from yarl import URL
import yaml
import logging
import re
from datetime import date, timedelta

from hackspace_mgmt.models import db, Label
from hackspace_mgmt.general.helpers import login_required

bp = Blueprint("label", __name__)

logger = logging.Logger(__name__)

@bp.route("/label")
@login_required
def index():
    return render_template("label.html")

@bp.route("/print")
@login_required
def print():
    label_type = request.args.get("label_type")

    now = date.today()

    if label_type == "short_stay":
        expiry = now + timedelta(days=30)
        caption = "Short stay"
    elif label_type == "project_box":
        expiry = now + timedelta(days=30*6)
        caption = "Project box"
    else:
        flash("Unknown label type")
        return redirect(url_for("general.index"))
    
    label = Label(
        member_id = g.member.id,
        expiry = expiry,
        caption = caption,
        printed = False,
    )
    db.session.add(label)
    db.session.commit()

    flash(f"Label has been printed. If it hasn't, check the printer is on.")
    return_url = url_for("label.index", _external=True)
    qs = {
        'return_url': return_url,
        'id': label.id
    }
    redir = URL("http://localhost:5000/print") % qs
    return redirect(redir)