
from flask import (
    Blueprint, abort, request, url_for, send_file, current_app
)
from .models import db, Member, Card, Machine, MachineController, Induction, InductionState
from sqlalchemy.exc import NoResultFound

bp = Blueprint('machine_api', __name__, url_prefix='/api/machines')

def controller_from_mac(machine_mac, join_machine=True):
    machine_mac = int(machine_mac, 16)
    machine_controller_query = db.select(MachineController).where(MachineController.mac==machine_mac)
    if join_machine:
        machine_controller_query = machine_controller_query.join(MachineController.machine)
    return db.one_or_404(machine_controller_query)


@bp.route('/<machine_mac>/unlock')
def unlock(machine_mac):
    controller = controller_from_mac(machine_mac)

    card_serial = int(request.args.get("card_id", "00000000"), 16)
    card_subq = db.select(Card).where(Card.card_serial==card_serial).subquery()
    member_query = db.select(Member).join(card_subq, Member.id==card_subq.c.member_id)
    member = db.one_or_404(member_query)

    try:
        induction = db.session.execute(db.select(Induction).where(Induction.member_id==member.id and Induction.machine_id==controller.machine.id)).scalar_one()
    except NoResultFound:
        abort(403)

    if induction.state != InductionState.valid:
        abort(403)

    return {"unlocked": True}

@bp.route('/<machine_mac>/lock')
def lock(machine_mac):
    return {"unlocked": False}

@bp.route('/<machine_mac>/status', methods=["POST"])
def status(machine_mac):
    machine_status = request.json

    controller = controller_from_mac(machine_mac)

    powered = machine_status.get("power")
    if powered is not None and powered != controller.powered:
        controller.powered = powered
        db.session.commit()
        if not powered:
            return {"unlocked": False}

    if controller.requires_update:
        controller.requires_update = False
        db.session.commit()
        return {"firmware_update": url_for('machine_api.firmware_update', _external=True)}

    return {}

@bp.route('/firmware_update')
def firmware_update():
    return send_file("/run/hackspace-mgmt/firmware_update.bin", as_attachment=True)


@bp.errorhandler(404)
def not_found_error(e):
    return {"unlocked": False}, 404