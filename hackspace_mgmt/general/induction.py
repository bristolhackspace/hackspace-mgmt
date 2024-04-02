from flask import Blueprint, render_template, g
import logging

from hackspace_mgmt.models import db, Machine, Induction, InductionState, LegacyMachineAuth
from hackspace_mgmt.general.helpers import login_required

bp = Blueprint("induction", __name__)

logger = logging.Logger(__name__)

@bp.route("/induction")
@login_required
def index():
    machine_select = db.select(Machine).where(Machine.hide_from_home == False).order_by(Machine.name)
    machines = db.session.scalars(machine_select).all()

    query = db.select(Machine.id).where(Machine.inductions.any(
        Induction.member_id==g.member.id and Induction.state == InductionState.valid
    ))
    inducted_machines = set(row.id for row in db.session.execute(query))

    return render_template("induction.html", machines=machines, inducted_machines=inducted_machines, LegacyMachineAuth=LegacyMachineAuth)