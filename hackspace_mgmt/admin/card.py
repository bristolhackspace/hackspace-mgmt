from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from hackspace_mgmt.models import db, Card, Member

class CardView(ModelView):
    column_list = ('number_on_front', 'card_serial', 'member')
    column_searchable_list = ('member.preferred_name', 'number_on_front')
    form_ajax_refs = {
        'member': QueryAjaxModelLoader('member', db.session, Member, fields=['preferred_name'], page_size=10, placeholder="Please select member")
    }

    def search_placeholder(self):
        return "Member or number"

def create_views(admin: Admin):
    admin.add_view(CardView(Card, db.session, category="Access Control"))