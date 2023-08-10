from flask_admin import form, Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
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

    inline_models = [
        (Card, dict(form_overrides = {"card_serial": SerialField}))
    ]

    column_labels = column_labels

    column_descriptions = column_descriptions

    form_widget_args = {
        "preferred_name": {
            "placeholder": "(optional)"
        }
    }

    def search_placeholder(self):
        return "Member name or email"

    def is_accessible(self):
        return request.headers.get("X-Remote-User") == "admin"


class NewMemberForm(form.BaseForm):
    first_name = fields.StringField(
        validators=[DataRequired()],
        render_kw={"autocomplete": "off"}
    )
    last_name = fields.StringField()
    preferred_name = fields.StringField(
        column_labels["preferred_name"],
        description=column_descriptions["preferred_name"],
        render_kw={
            "placeholder": "(optional)",
            "autocomplete": "off"
        }
    )
    email = fields.EmailField(
        validators=[DataRequired()],
        render_kw={"autocomplete": "off"}
    )
    card_number = fields.IntegerField(
        'Number on front of card/keyfob',
        render_kw={"autocomplete": "off"}
    )

class NewMemberView(BaseView):

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        return_url = get_redirect_target() or self.get_url('.index')

        member_form = NewMemberForm(request.form)

        if validate_form_on_submit(member_form):
            new_member = Member(
                first_name = member_form.first_name.data,
                last_name = member_form.last_name.data,
                preferred_name = member_form.preferred_name.data,
                email = member_form.email.data,
            )
            db.session.add(new_member)
            db.session.commit()

            card_update = db.update(Card).where(Card.number_on_front==member_form.card_number.data)
            card_update = card_update.values(member_id=new_member.id)
            result = db.session.execute(card_update)
            if not result.rowcount:
                card = Card(
                    number_on_front=member_form.card_number.data,
                    member_id=new_member.id
                )
                db.session.add(card)
                card_type = "unenrolled"
            else:
                card_type = "pre-enrolled"
            db.session.commit()

            flash(f'New member created with {card_type} card.', 'success')
            return redirect(return_url)

        return self.render('admin/new_member.html', return_url=return_url, form=member_form)


def create_views(admin: Admin):
    admin.add_view(MemberView(Member, db.session, category="Membership"))
    admin.add_view(NewMemberView("New Member", endpoint="new_member", category="Membership"))

