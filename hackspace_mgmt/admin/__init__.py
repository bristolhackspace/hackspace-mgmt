from flask_admin import Admin

from . import machine, induction, firmware_update, card, bulk_card, member, label, quiz

admin = Admin(None, 'Hackspace Management Admin', template_mode='bootstrap4', endpoint="admin", url="/admin")

machine.create_views(admin)
induction.create_views(admin)
firmware_update.create_views(admin)
card.create_views(admin)
bulk_card.create_views(admin)
member.create_views(admin)
label.create_views(admin)
quiz.create_views(admin)