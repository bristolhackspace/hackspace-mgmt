from flask_admin import Admin, expose
from flask_admin.form import RenderTemplateWidget, DatePickerWidget
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.helpers import get_redirect_target
from flask_admin.model.template import EndpointLinkRowAction
from flask_admin.model.helpers import get_mdict_item_or_list
from flask import request, flash, redirect
from hackspace_mgmt.models import db, Member, Card
from hackspace_mgmt.forms import ViewHelperJsMixin
from wtforms import fields, validators
from datetime import date
import logging

log = logging.getLogger(__name__)

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

class CheckboxListField(fields.SelectMultipleField):
    widget = RenderTemplateWidget("admin/checkbox_list.html")

class MemberView(ViewHelperJsMixin, ModelView):
    can_view_details = True
    can_export = True
    column_list = member_columns
    form_columns = member_columns
    column_filters = member_columns
    column_details_list = member_columns
    column_searchable_list = (
        'first_name',
        'last_name',
        'preferred_name',
        'email',
        'alt_email'
    )

    form_ajax_refs = {
        'cards': QueryAjaxModelLoader('cards', db.session, Card, fields=['number_on_front'], page_size=10, placeholder="####", minimum_input_length=3),
    }

    column_labels = column_labels

    column_descriptions = column_descriptions

    form_widget_args = {
        "preferred_name": {
            "placeholder": "(optional)"
        }
    }

    form_create_rules = ('first_name', 'last_name', 'preferred_name', 'email', 'cards')

    column_extra_row_actions = [
        EndpointLinkRowAction('fa fa-sign-out', '.offboard_view', "Offboard member")
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._offboard_form_class = self.get_offboard_form()


    def search_placeholder(self):
        return "Member name or email"

    # def is_accessible(self):
    #     return request.headers.get("X-Remote-User") == "admin"


    def get_offboard_form(self):
        class OffboardForm(self.form_base_class):
            id = fields.HiddenField(validators=[validators.InputRequired()])
            url = fields.HiddenField()
            end_reason = fields.StringField("End reason")
            end_date = fields.DateField("End date", widget=DatePickerWidget(), validators=[validators.DataRequired()])
            returned_cards = CheckboxListField("Select the cards that have been returned")

        return OffboardForm

    def offboard_form(self, **kwargs):
        if request.form:
            return self._offboard_form_class(request.form)
        else:
            return self._offboard_form_class(**kwargs)

    
    @expose('/offboard/', methods=('GET', 'POST'))
    def offboard_view(self):
        """
            Offboard model view
        """
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_edit:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)

        form = self.offboard_form(
            id=model.id,
            end_reason=model.end_reason,
            end_date=model.end_date or date.today(),
        )

        card_choices = [(str(card.id), card.number_on_front) for card in model.cards]
        form.returned_cards.choices = card_choices

        if self.validate_form(form):
            try:
                model.end_reason = form.end_reason.data
                model.end_date = form.end_date.data
                for card in model.cards:
                    if str(card.id) in form.returned_cards.data:
                        card.member_id = None
                    else:
                        card.lost = True
                self.session.commit()
                flash(gettext('Record was successfully saved.'), 'success')
            except Exception as ex:
                if not self.handle_view_exception(ex):
                    flash(gettext('Failed to update record. %(error)s', error=str(ex)), 'error')
                    log.exception('Failed to update record.')

                self.session.rollback()
            
            return redirect(self.get_save_return_url(model, is_created=False))

        return self.render("admin/member_offboard.html",
                           model=model,
                           form=form,
                           return_url=return_url)



def create_views(admin: Admin):
    admin.add_view(MemberView(Member, db.session, category="Membership"))

