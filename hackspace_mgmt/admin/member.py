from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import request, url_for
from hackspace_mgmt.models import db, Member, Card
from hackspace_mgmt.admin.card import SerialField


member_columns = (
    "first_name",
    "last_name",
    "preferred_name",
    "email",
    "alt_email",
    "join_date",
    "discourse",
    "newsletter",
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
)

class MemberView(ModelView):
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

    inline_models = [
        (Card, dict(form_overrides = {"card_serial": SerialField}))
    ]

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


    form_widget_args = {
        "preferred_name": {
            "placeholder": "(optional)"
        }
    }

    def render(self, template, **kwargs):
        """
        using extra js in render method allow use
        url_for that itself requires an app context
        """
        self.extra_js = [url_for("static", filename="js/helpers.js")]

        return super().render(template, **kwargs)

    def search_placeholder(self):
        return "Member name or email"

    def is_accessible(self):
        return request.headers.get("X-Remote-User") == "admin"

def create_views(admin: Admin):
    admin.add_view(MemberView(Member, db.session, category="Access Control"))
