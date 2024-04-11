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

@bp.route("/create")
@login_required
def create():
    label_type = request.args.get("label_type")

    now = date.today()

    if label_type == "short_stay":
        expiry = now + timedelta(days=30)
        caption = "Short stay"
    elif label_type == "project_box":
        expiry = now + timedelta(days=30*6)
        caption = "Project box"
    else:
        return {"error": "unknown label type"}, 400
    
    label = Label(
        member_id = g.member.id,
        expiry = expiry,
        caption = caption,
        printed = False,
    )
    db.session.add(label)
    db.session.commit()

    return {
        "status": "success",
        "label": {
            "id": label.id,
            "name": str(g.member),
            "expiry": label.expiry.strftime("%d %b %Y"),
            "caption": label.caption
        }
    }