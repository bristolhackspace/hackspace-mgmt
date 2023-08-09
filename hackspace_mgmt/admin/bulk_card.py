
from wtforms import fields
from wtforms.validators import DataRequired
from flask import flash, request
from flask_admin import form, Admin, BaseView, expose
from flask_admin.helpers import get_redirect_target, validate_form_on_submit
from hackspace_mgmt.models import db, Card
from hackspace_mgmt.forms import SerialField
from werkzeug.datastructures import MultiDict
from sqlalchemy.exc import NoResultFound

class CardInfoForm(form.BaseForm):
    number_on_front = fields.IntegerField(
        'Number on front of card/keyfob',
        validators=[DataRequired()],
        render_kw={"autofocus": "1", "autocomplete": "off"}
    )

    intermediate = True


class CardSerialForm(CardInfoForm):
    serial_number = SerialField(
        'Scan card',
        suppress_enter=False,
        render_kw={"autofocus": "1", "autocomplete": "off"},
    )
    number_on_front = fields.HiddenField(validators=[DataRequired()])

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
            number_on_front = int(serial_form.number_on_front.data)
            serial_number = serial_form.serial_number.data

            card_update = db.update(Card).where(Card.number_on_front==number_on_front)
            card_update = card_update.values(card_serial=serial_number)
            result = db.session.execute(card_update)
            if not result.rowcount:
                card = Card(
                    number_on_front=number_on_front,
                    card_serial=serial_number
                )
                db.session.add(card)
                action = "created"
            else:
                action = "updated"
            db.session.commit()

            flash(f'Card {serial_form.number_on_front.data} {action} successfully', 'success')
            next_num = int(serial_form.number_on_front.data) + 1
            info_form = CardInfoForm(MultiDict({"number_on_front": next_num}))
            return self.render('admin/bulk_card.html', return_url=return_url, form=info_form)
        
        info_form = CardInfoForm(request.form)

        if validate_form_on_submit(info_form):
            return self.render('admin/bulk_card.html', return_url=return_url, form=serial_form)
            
        return self.render('admin/bulk_card.html', return_url=return_url, form=info_form)


def create_views(admin: Admin):
    admin.add_view(EnrollCardView("Bulk card enroll", endpoint="bulk_card", category="Membership"))