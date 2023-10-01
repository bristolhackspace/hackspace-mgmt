from flask_admin import form, Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.helpers import get_redirect_target, validate_form_on_submit
from flask import request, flash, redirect
from hackspace_mgmt.models import db, Member, Card
from hackspace_mgmt.forms import SerialField, ViewHelperJsMixin
from wtforms import fields
from wtforms.validators import DataRequired

member_columns = (
    "first_name",
    "last_name",
    "preferred_name",
    "email",
    "alt_email",
    "join_date",
    "discourse",
    "newsletter",
    "welcome_email_sent",
    "payment_ref",
    "payment_active",
    "address1",
    "address2",
    "town_city",
    "county",
    "postcode",
    "end_date",
    "end_reason",
    "notes",
    "cards",
)

column_labels = {
    'preferred_name': "Preferred full name (including surname)",
    'discourse': "Discourse invite status",
    'newsletter': "Added to newsletter? (currently mailchimp)"
}

column_descriptions = {
    'preferred_name': (
        "This must include the surname unless the member uses a mononym." +
        " Leave blank if not needed."
    )
}

class MemberView(ViewHelperJsMixin, ModelView):
    can_view_details = True
    can_export = True
    column_list = member_columns
    form_columns = member_columns
    column_filters = member_columns
    column_details_list = member_columns + ("cards",)
    column_searchable_list = (
        'first_name',
        'last_name',
        'preferred_name',
        'email',
        'alt_email'
    )

    form_ajax_refs = {
        'cards': QueryAjaxModelLoader('cards', db.session, Card, fields=['number_on_front'], page_size=10, placeholder="####", minimum_input_length=4),
    }

    column_labels = column_labels

    column_descriptions = column_descriptions

    form_widget_args = {
        "preferred_name": {
            "placeholder": "(optional)"
        }
    }

    form_create_rules = ('first_name', 'last_name', 'preferred_name', 'email', 'cards')


    def search_placeholder(self):
        return "Member name or email"

    def is_accessible(self):
        return request.headers.get("X-Remote-User") == "admin"


def create_views(admin: Admin):
    admin.add_view(MemberView(Member, db.session, category="Membership"))

