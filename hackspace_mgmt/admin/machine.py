from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from hackspace_mgmt.models import db, Machine, MachineController
from flask_admin.model.form import InlineFormAdmin


class MachineView(ModelView):
    column_searchable_list = ['name']
    column_list = ('name', 'controllers')
    inline_models = (MachineController,)
    form_excluded_columns = ('inductions',)
    column_formatters = dict()


def create_views(admin: Admin):
    admin.add_view(MachineView(Machine, db.session, endpoint="admin/machine", category="Access Control"))