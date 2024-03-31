
from flask import Blueprint
from .models import db, Label

bp = Blueprint('label_api', __name__, url_prefix='/api/labels')

@bp.route('/label/<int:label_id>')
def label(label_id):
    query = db.select(Label).where(Label.id==label_id)
    label = db.one_or_404(query)

    response = {
        "id": label.id,
        "name": str(label.member),
        "expiry": label.expiry.strftime("%d %b %Y"),
        "caption": label.caption,
        "printed": label.printed
    }

    return response