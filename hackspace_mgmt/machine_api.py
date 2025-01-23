
from flask import (
    Blueprint, abort, request, url_for, send_file, current_app
)

from hackspace_mgmt.audit import create_audit_log
from .models import db, Member, Card, Machine, MachineController, Induction
from sqlalchemy.exc import NoResultFound
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timezone
import logging

bp = Blueprint('machine_api', __name__, url_prefix='/api/machines')

def controller_from_hostname(hostname, join_machine=True) -> MachineController:
    machine_controller_query = db.select(MachineController).where(MachineController.hostname==hostname)
    if join_machine:
        machine_controller_query = machine_controller_query.join(MachineController.machine)
    return db.one_or_404(machine_controller_query)


def format_card_serial(card_id_str):
    if card_id_str is None:
        card_id_str = "00000000"
    if "-" in card_id_str:
        parts = card_id_str.split("-")
        card_id_str = "".join(parts[::-1])

    current_app.logger.info(f"Serial string is {card_id_str}")
    return int(card_id_str, 16)


@bp.route('/<hostname>/unlock')
def unlock(hostname):
    controller = controller_from_hostname(hostname)

    current_app.logger.debug(f"Controller is {controller}")

    card_serial = format_card_serial(request.args.get("card_id"))
    card_subq = db.select(Card).where(Card.card_serial==card_serial).subquery()
    member_query = db.select(Member).join(card_subq, Member.id==card_subq.c.member_id)
    member = db.one_or_404(member_query)

    current_app.logger.debug(f"Member is {member}")
    current_app.logger.debug(f"Machine ID is {controller.machine.id}")

    if not controller.machine.is_member_inducted(member):
        create_audit_log(
            "access_control",
            "unlock_denied",
            data = {
                "controller": {
                    "id": controller.id,
                    "hostname": controller.hostname
                },
                "machine": {
                    "id": controller.machine.id,
                    "name": controller.machine.name
                },
            },
            member=member
        )
        current_app.logger.info(f"'{member}' ({member.id}) unauthorized unlock attempt for {controller.machine.name} ({hostname})")
        abort(403)
    else:
        create_audit_log(
            "access_control",
            "unlock_success",
            data = {
                "controller": {
                    "id": controller.id,
                    "hostname": controller.hostname
                },
                "machine": {
                    "id": controller.machine.id,
                    "name": controller.machine.name
                },
            },
            member=member
        )
        current_app.logger.info(f"'{member}' ({member.id}) successfully unlocked {controller.machine.name} ({hostname})")

    return {"unlocked": True}

@bp.route('/<hostname>/lock')
def lock(hostname):
    controller = controller_from_hostname(hostname)
    current_app.logger.info(f"Lock button pressed on {controller.machine.name} ({hostname})")
    return {"unlocked": False}

@bp.route('/<hostname>/enroll')
def enroll(hostname):
    controller = controller_from_hostname(hostname)

    current_app.logger.debug(f"Controller is {controller}")

    inductor_card = format_card_serial(request.args.get("inductor_id"))
    card_subq = db.select(Card).where(Card.card_serial==inductor_card).subquery()
    member_query = db.select(Member).join(card_subq, Member.id==card_subq.c.member_id)
    inductor = db.one_or_404(member_query)

    current_app.logger.debug(f"Inductor is {inductor}")
    current_app.logger.debug(f"Machine ID is {controller.machine.id}")


    inductee_card_str = request.args.get("inductee_id")
    if inductee_card_str is None:
        return {}

    inductee_card = format_card_serial(inductee_card_str)
    card_subq = db.select(Card).where(Card.card_serial==inductee_card).subquery()
    member_query = db.select(Member).join(card_subq, Member.id==card_subq.c.member_id)
    inductee = db.session.execute(member_query).scalar_one()


    if not controller.machine.is_member_inducted(inductor, check_can_induct=True):
        create_audit_log(
            "access_control",
            "enroll_denied",
            data = {
                "controller": {
                    "id": controller.id,
                    "hostname": controller.hostname
                },
                "machine": {
                    "id": controller.machine.id,
                    "name": controller.machine.name
                },
                "inductee": inductee.id if inductee else None
            },
            member=inductor
        )
        current_app.logger.info(f"'{inductor}' ({inductor.id}) unauthorized to induct for {controller.machine.name} ({hostname})")
        abort(403)
    else:
        current_app.logger.info(f"'{inductor}' ({inductor.id}) authorised to induct for {controller.machine.name} ({hostname})")


    if not inductee:
        abort(404)


    now=datetime.now(timezone.utc)
    upsert_stmt = insert(Induction).values(
        member_id=inductee.id,
        machine_id=controller.machine.id,
        inducted_by=inductor.id,
        inducted_on=now
    ).on_conflict_do_update(
        index_elements=[Induction.member_id, Induction.machine_id],
        set_=dict(
            inducted_by=inductor.id,
            inducted_on=now
        ),
    )
    db.session.execute(upsert_stmt)

    create_audit_log(
        "access_control",
        "enroll_success",
        data = {
            "controller": {
                "id": controller.id,
                "hostname": controller.hostname
            },
            "machine": {
                "id": controller.machine.id,
                "name": controller.machine.name
            },
            "inductee": inductee.id
        },
        logged_at=now,
        member=inductor,
        commit=False
    )

    db.session.commit()

    return {}



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

@bp.route('/<hostname>/has_update')
def has_update(hostname):
    controller = controller_from_hostname(hostname)
    if controller.requires_update:
        controller.requires_update = False
        db.session.commit()
        return {"update_url": url_for('machine_api.firmware_update', _external=True)}
    else:
        return {}


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