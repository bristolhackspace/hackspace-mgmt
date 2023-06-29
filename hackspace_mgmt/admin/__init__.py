from flask_admin import Admin
from . import machine, induction, firmware_update, card, enroll_card

admin = Admin(None, 'Hackspace Management Portal', template_mode='bootstrap4', url="/")

machine.create_views(admin)
induction.create_views(admin)
firmware_update.create_views(admin)
card.create_views(admin)
enroll_card.create_views(admin)