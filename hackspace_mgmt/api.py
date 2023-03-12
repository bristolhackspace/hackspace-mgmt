
from flask import (
    Blueprint, render_template, jsonify, request
)

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/machines/<machine_id>/unlock')
def unlock(machine_id):
    card_id = request.args.get("card_id", "")
    return jsonify({
        "machine": machine_id,
        "card": card_id
    })

@bp.route('/machines/<machine_id>/lock')
def lock(machine_id):
    return jsonify({})