from flask import (
    Blueprint, render_template, jsonify, request
)
from dataclasses import dataclass

bp = Blueprint('equipment', __name__, url_prefix='/equipment')

@dataclass
class Equipment:
    name: str
    has_quiz: bool


equipment_list = [
    Equipment("CNC Mill", False),
    Equipment("Laser Cutter", False),
    Equipment("Bandsaw", False),
    Equipment("Mitre Saw", True),
    Equipment("Table Saw", True),
    Equipment("3D Printers", False),
]

@bp.route('/')
def index():
    return render_template('equipment/index.html', equipment=equipment_list)