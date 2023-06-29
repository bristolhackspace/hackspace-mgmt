
from wtforms import fields, validators
from flask import flash, redirect, request
from flask_admin import form, Admin, BaseView, expose
from flask_admin.helpers import get_redirect_target, validate_form_on_submit
from hackspace_mgmt.models import db, Card, Member
from sqlalchemy.exc import NoResultFound


class EnrollCardForm(form.BaseForm):
    number_on_front = fields.IntegerField('Number on front of card')
    serial_number = fields.StringField('Scan card to enter serial number', render_kw={'accesskey': 'n'})


class EnrollCardView(BaseView):

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = EnrollCardForm(request.form)
        return_url = get_redirect_target() or self.get_url('.index')

        default_render = lambda: self.render('enroll_card.html', return_url=return_url, form=form)
            

        if not validate_form_on_submit(form):
            return default_render()
        
        number_on_front = form.number_on_front.data
        serial_number = form.serial_number.data

        try:
            serial_number = int(serial_number, 16)
        except ValueError:
            flash("Invalid serial number", "error")
            return default_render()

        card_select = db.select(Card).where(Card.number_on_front==number_on_front)
        try:
            card = db.session.execute(card_select).scalar_one()
        except NoResultFound:
            card = None

        if card is None or card.card_serial is not None:
            flash(f"Card {number_on_front} already registered. " +
                "If this wasn't you and your card doesn't work then " +
                "contact the Hackspace committee.",
                "error"
            )
            return default_render()

        card.card_serial = serial_number
        db.session.commit()
        flash(f'Card {number_on_front} registered successfully', 'success')
        return redirect(return_url)


def create_views(admin: Admin):
    admin.add_view(EnrollCardView("Enroll card", endpoint="enroll"))