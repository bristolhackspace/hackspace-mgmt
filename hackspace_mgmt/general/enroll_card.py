
from wtforms import fields, ValidationError
from wtforms.validators import EqualTo, DataRequired
from flask import flash, redirect, request
from flask_admin import form, Admin, BaseView, expose
from flask_admin.helpers import get_redirect_target, validate_form_on_submit, get_form_data
from hackspace_mgmt.models import db, Card, Member
from hackspace_mgmt.forms import SerialField
from sqlalchemy.exc import NoResultFound


class CardInfoForm(form.BaseForm):
    number_on_front = fields.IntegerField(
        'Number on front of card',
        validators=[DataRequired()],
        render_kw={"autocomplete": "off"}
    )
    number_on_front_verify = fields.IntegerField(
        'Confirm number on front of card', 
        validators=[EqualTo("number_on_front", "Values do not match")],
        render_kw={"autocomplete": "off"}
    )
    email = fields.EmailField(
        "Email you signed up with",
        validators=[DataRequired()],
        render_kw={"autocomplete": "off"}
    )

    intermediate = True

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False

        number_on_front = self.number_on_front.data

        card_select = db.select(Card).where(Card.number_on_front==number_on_front)
        card_select = card_select.join(Card.member)
        try:
            card = db.session.execute(card_select).scalar_one()
        except NoResultFound:
            card = None

        if (
            card is None
            or card.member is None
            or self.email.data not in [card.member.email, card.member.alt_email]
        ):
            self.email.errors.append("Incorrect email for card")
            return False

        if card.card_serial is not None:
            self.number_on_front.errors.append(f"Card already registered")
            return False

        self.card = card

        return True


class CardSerialForm(CardInfoForm):
    serial_number = SerialField(
        'Remove card/fob from wallet (if applicable) and scan to enter serial number',
        suppress_enter=False,
        render_kw={"autofocus": "1", "autocomplete": "off"},
        description="Removing from wallet is required to avoid accidentally scanning the wrong card"
    )
    number_on_front = fields.HiddenField(validators=[DataRequired()])
    number_on_front_verify = fields.HiddenField()
    email = fields.HiddenField(validators=[DataRequired()])

    intermediate = False

    def validate(self, extra_validators=None):
        self.serial_number.flags.required = True

        if not super().validate(extra_validators=extra_validators):
            return False

        if not self.serial_number.raw_data:
            return False

        if self.serial_number.data is None:
            self.serial_number.errors.append(
                self.serial_number.gettext("This field is required.")
            )
            return False

        return True


class EnrollCardView(BaseView):

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        return_url = get_redirect_target() or self.get_url('.index')

        serial_form = CardSerialForm(request.form)

        if validate_form_on_submit(serial_form):
            card = serial_form.card
            card.card_serial = serial_form.serial_number.data
            db.session.commit()
            flash(f'Card {serial_form.number_on_front.data} registered successfully', 'success')
            return redirect(return_url)
        
        info_form = CardInfoForm(request.form)

        if validate_form_on_submit(info_form):
            return self.render('enroll_card.html', return_url=return_url, form=serial_form)
            
        return self.render('enroll_card.html', return_url=return_url, form=info_form)


def create_views(admin: Admin):
    admin.add_view(EnrollCardView("Enroll card", endpoint="enroll"))