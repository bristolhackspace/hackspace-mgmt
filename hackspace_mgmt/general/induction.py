from flask import Blueprint, render_template, g
import logging

from hackspace_mgmt.models import db, Machine, Induction, LegacyMachineAuth, Member
from hackspace_mgmt.general.helpers import login_required

bp = Blueprint("induction", __name__)

logger = logging.Logger(__name__)

@bp.route("/induction")
@login_required
def index():
    machine_select = db.select(Machine).where(Machine.hide_from_home == False).order_by(Machine.name)
    machines = db.session.scalars(machine_select).all()

    return render_template("induction.html", machines=machines, LegacyMachineAuth=LegacyMachineAuth)

@bp.route("/induction/<int:machine_id>")
@login_required
def machine(machine_id):
    machine = db.get_or_404(Machine, machine_id)

    member: Member = g.member

    completed_quizes = set(completion.quiz for completion in member.quiz_completions if not completion.has_expired())
    expired_quizes = set(completion.quiz for completion in member.quiz_completions if completion.has_expired())

    induction = None
    for member_induction in member.inductions:
        if member_induction.machine == machine:
            induction = member_induction
            break

    return render_template(
        "machine_induction.html",
        machine=machine,
        completed_quizes=completed_quizes,
        expired_quizes=expired_quizes,
        induction=induction,
        LegacyMachineAuth=LegacyMachineAuth
    )