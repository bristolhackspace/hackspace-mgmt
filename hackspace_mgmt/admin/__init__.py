from flask_admin import Admin
from . import machine, induction

admin = Admin(None, 'Hackspace Management Portal', template_mode='bootstrap4', url="/")

machine.create_views(admin)
induction.create_views(admin)
