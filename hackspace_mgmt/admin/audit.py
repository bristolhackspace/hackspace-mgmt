from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from hackspace_mgmt.models import AuditLog, db
from hackspace_mgmt.forms import ViewHelperJsMixin


class AuditView(ViewHelperJsMixin, ModelView):
    column_list = ('logged_at', 'member', 'category', 'event')
    column_searchable_list = ('member.display_name',)
    column_filters = ('category', 'event')

    can_create=False
    can_edit=False
    can_delete=False
    can_view_details=True

    def search_placeholder(self):
        return "Member name"

def create_views(admin: Admin):
    admin.add_view(AuditView(AuditLog, db.session, endpoint="audit_view", category="Audit"))