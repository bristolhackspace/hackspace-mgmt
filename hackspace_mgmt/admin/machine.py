from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from hackspace_mgmt.models import db, Machine

class MachineView(ModelView):
    can_view_details = True
    column_searchable_list = ['name']
    column_list = ('name', 'controllers')
    column_details_list = ('name', 'controllers')

    # def _controller_formatter(view, context, model, name):
    #     return Markup(
    #         "<a href='{}'>{}</a>".format(
    #             url_for('machine_controller.details_view', id=model.member.id),
    #             escape(model.member)
    #         )
    #     ) if model.member else u""

    # column_formatters = {
    #     'controllers': _controller_formatter
    # }

def create_views(admin: Admin):
    admin.add_view(MachineView(Machine, db.session, category="Access Control"))