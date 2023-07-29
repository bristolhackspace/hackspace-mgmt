from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from hackspace_mgmt.models import db, Card, Member
from hackspace_mgmt.forms import SerialField, card_serial_formatter, ViewHelperJsMixin


class CardView(ViewHelperJsMixin, ModelView):
    column_list = ('number_on_front', 'card_serial', 'member')
    column_searchable_list = ('member.display_name', 'number_on_front')
    form_ajax_refs = {
        'member': QueryAjaxModelLoader('member', db.session, Member, fields=['display_name'], page_size=10, placeholder="Please select member")
    }

    form_overrides = {
        "card_serial": SerialField
    }

    column_formatters = {
        "card_serial": card_serial_formatter
    }

    def search_placeholder(self):
        return "Member or number"

def create_views(admin: Admin):
    admin.add_view(CardView(Card, db.session, category="Access Control"))