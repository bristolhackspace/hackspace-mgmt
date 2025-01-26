from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from hackspace_mgmt.models import db, Machine, MachineController
from flask_admin.model.form import InlineFormAdmin


class MachineView(ModelView):
    column_searchable_list = ['name']
    column_list = ('name', 'controllers', 'requires_in_person', 'valid_for_days', 'hide_from_home', 'quizzes')
    inline_models = (MachineController,)
    form_excluded_columns = ('inductions',)
    column_formatters = dict()


def create_views(admin: Admin):
    admin.add_view(MachineView(Machine, db.session, endpoint="machine_view", category="Access Control"))