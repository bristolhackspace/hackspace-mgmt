from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from hackspace_mgmt.models import db, Card, Member
from wtforms import Field, widgets
from flask import url_for

class SerialField(Field):
    """
    A text field, except all input is coerced to an integer.  Erroneous input
    is ignored and will not be accepted as a value.
    """

    widget = widgets.TextInput()

    def __init__(self, label=None, validators=None, render_kw=None, **kwargs):
        render_kw = render_kw or {}
        render_kw["data-suppress-enter"] = "1"
        super().__init__(label, validators, render_kw=render_kw, **kwargs)

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data is not None:
            return f'{self.data:x}'
        return ""

    def process_formdata(self, valuelist):
        if not valuelist:
            return

        try:
            self.data = int(valuelist[0], 16)
        except ValueError as exc:
            self.data = None
            raise ValueError(self.gettext("Not a valid serial number.")) from exc

def card_serial_formatter(view, context, model, name):
    if model.card_serial:
        return f"{model.card_serial:x}"
    else:
        return ""


class CardView(ModelView):
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

    def render(self, template, **kwargs):
        """
        using extra js in render method allow use
        url_for that itself requires an app context
        """
        self.extra_js = [url_for("static", filename="js/helpers.js")]

        return super().render(template, **kwargs)


    def search_placeholder(self):
        return "Member or number"

def create_views(admin: Admin):
    admin.add_view(CardView(Card, db.session, category="Access Control"))