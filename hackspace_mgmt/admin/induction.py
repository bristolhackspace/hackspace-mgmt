from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from hackspace_mgmt.models import db, Induction, Member

class InductionView(ModelView):
    can_view_details = True
    column_list = ('member', 'machine', 'state')
    form_ajax_refs = {
        'member': QueryAjaxModelLoader('member', db.session, Member, fields=['preferred_name'], page_size=10, placeholder="Please select member")
    }

def create_views(admin: Admin):
    admin.add_view(InductionView(Induction, db.session, category="Access Control"))