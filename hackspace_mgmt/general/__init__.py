from flask_admin import Admin
from . import enroll_card

general = Admin(None, 'Hackspace Management Portal', template_mode='bootstrap4', endpoint="general", url="/")

enroll_card.create_views(general)