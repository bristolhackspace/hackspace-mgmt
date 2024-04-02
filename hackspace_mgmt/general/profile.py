from flask import Blueprint, flash, redirect, render_template, url_for, request, g
from flask_wtf import FlaskForm
from wtforms import fields, validators
import logging

from hackspace_mgmt.models import db, Member
from hackspace_mgmt.general.helpers import login_required

bp = Blueprint("profile", __name__)

logger = logging.Logger(__name__)


class ProfileForm(FlaskForm):
    submit_label = "Update"

    first_name = fields.StringField('First name', [validators.ReadOnly()])
    last_name = fields.StringField('Last name', [validators.ReadOnly()])
    preferred_name = fields.StringField('Preferred name', [validators.Length(max=Member.preferred_name.type.length)])
    email = fields.EmailField('Email', [validators.ReadOnly()])
    join_date = fields.DateField("Join date", [validators.ReadOnly()])

    address1 = fields.StringField("Address 1", [validators.ReadOnly()])
    address2 = fields.StringField("Address 2", [validators.ReadOnly()])
    town_city = fields.StringField("Town/City", [validators.ReadOnly()])
    county = fields.StringField("County", [validators.ReadOnly()])
    postcode = fields.StringField("Postcode", [validators.ReadOnly()])



@bp.route("/profile", methods=["POST","GET"])
@login_required
def index():
    profile_form = ProfileForm(request.form, obj=g.member)

    if profile_form.validate_on_submit():
          g.member.preferred_name = profile_form.preferred_name.data
          db.session.commit()
          flash("Profile updated")
          return redirect(url_for(".index"))


    return render_template("profile.html", profile_form=profile_form, return_url=url_for("general.index"))