from flask_admin import Admin, AdminIndexView
from . import enroll_card

general = Admin(
    None,
    'Hackspace Management Portal',
    template_mode='bootstrap4',
    index_view=AdminIndexView(
        endpoint='general',
        template='general/index.html',
        url='/'
    )
)

enroll_card.create_views(general)