
from flask import (
    Blueprint, render_template
)

bp = Blueprint('general', __name__, url_prefix='/general')

@bp.route('/enroll_card')
def enroll_card():
    return render_template('general/enroll_card.html')

