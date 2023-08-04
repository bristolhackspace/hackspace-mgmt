from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from hackspace_mgmt.models import db, Label, Member


class LabelView(ModelView):
    form_ajax_refs = {
        'member': QueryAjaxModelLoader('member', db.session, Member, fields=['display_name'], page_size=10, placeholder="Please select member"),
        }


def create_views(admin: Admin):
    admin.add_view(LabelView(Label, db.session, category="Access Control"))