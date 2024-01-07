
from flask import (
    Blueprint, abort, request, url_for, send_file, current_app
)
from .models import db, Member, Card, Machine, MachineController, Induction, InductionState
from sqlalchemy.exc import NoResultFound
import logging

bp = Blueprint('machine_api', __name__, url_prefix='/api/machines')

def controller_from_hostname(hostname, join_machine=True):
    machine_controller_query = db.select(MachineController).where(MachineController.hostname==hostname)
    if join_machine:
        machine_controller_query = machine_controller_query.join(MachineController.machine)
    return db.one_or_404(machine_controller_query)


@bp.route('/<hostname>/unlock')
def unlock(hostname):
    controller = controller_from_hostname(hostname)

    current_app.logger.debug(f"Controller is {controller}")

    card_id_str = request.args.get("card_id", "00000000")
    if "-" in card_id_str:
        parts = card_id_str.split("-")
        card_id_str = "".join(parts[::-1])

    current_app.logger.info(f"Serial string is {card_id_str}")

    card_serial = int(card_id_str, 16)
    card_subq = db.select(Card).where(Card.card_serial==card_serial).subquery()
    member_query = db.select(Member).join(card_subq, Member.id==card_subq.c.member_id)
    member = db.one_or_404(member_query)

    current_app.logger.debug(f"Member is {member}")
    current_app.logger.debug(f"Machine ID is {controller.machine.id}")

    try:
        induction = db.session.execute(
            db.select(Induction)
                .where(Induction.member_id==member.id)
                .where(Induction.machine_id==controller.machine.id)
        ).scalar_one()
        current_app.logger.debug(f"Inductions: {induction}")

        current_app.logger.info(f"'{member}' ({member.id}) successfully unlocked {controller.machine.name} ({hostname})")
    except NoResultFound:
        current_app.logger.info(f"'{member}' ({member.id}) unauthorized unlock attempt for {controller.machine.name} ({hostname})")
        abort(403)

    if induction.state != InductionState.valid:
        abort(403)

    return {"unlocked": True}

@bp.route('/<hostname>/lock')
def lock(hostname):
    controller = controller_from_hostname(hostname)
    current_app.logger.info(f"Lock button pressed on {controller.machine.name} ({hostname})")
    return {"unlocked": False}

@bp.route('/<hostname>/status', methods=["POST"])
def status(hostname):
    machine_status = request.json

    controller = controller_from_hostname(hostname)

    current_app.logger.debug(f"Status request: {machine_status}")

    response = {}

    has_settings = machine_status.get("has_settings", True)
    if not has_settings:
        response["idle_timeout"] = controller.idle_timeout
        response["idle_power_threshold"] = controller.idle_power_threshold
        response["invert_logout_button"] = controller.invert_logout_button


    if controller.requires_update:
        controller.requires_update = False
        db.session.commit()
        # Override all other responses
        return {"firmware_update": url_for('machine_api.firmware_update', _external=True)}

    current_app.logger.debug(f"Status response: {response}")

    return response


@bp.route('/<hostname>/settings')
def settings(hostname):

    controller = controller_from_hostname(hostname)

    response = {}

    response["idle_timeout"] = controller.idle_timeout
    response["idle_power_threshold"] = controller.idle_power_threshold

    current_app.logger.debug(f"Settings response: {response}")

    return response

@bp.route('/firmware_update')
def firmware_update():
    return send_file("/run/hackspace-mgmt/firmware_update.bin", as_attachment=True)

@bp.errorhandler(403)
def not_authorized_error(e):
    return {"unlocked": False}, 403

@bp.errorhandler(404)
def not_found_error(e):
    return {"unlocked": False}, 404