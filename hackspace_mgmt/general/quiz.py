from flask import Blueprint, flash, redirect, render_template, url_for, request, g
from flask_wtf import FlaskForm
from markupsafe import Markup, escape
from wtforms import fields, widgets, ValidationError
from wtforms.validators import InputRequired
from sqlalchemy.dialects.postgresql import insert
import yaml
import logging
import re
from datetime import date

from hackspace_mgmt.models import db, Quiz, Member, Induction, InductionState
from hackspace_mgmt.general.helpers import login_required

bp = Blueprint("quiz", __name__)

logger = logging.Logger(__name__)

class Exactly:
    def __init__(self, value, message=None):
            self.value = value
            self.message = message

    def __call__(self, form, field):
        if isinstance(self.value, set) and set(field.data) == self.value:
            return
        elif field.data == self.value:
            return
        message = self.message
        if message is None:
            message = "Incorrect answer"
        raise ValidationError(message)

class MultiCheckboxField(fields.SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


LINK_MD_REGEX = re.compile(r"\[\[(?P<url>[^|]+)\|(?P<text>[^\]]+)\]\]")
IMAGE_MD_REGEX = re.compile(r"\{\{(?P<link>[^}]+)\}\}")

WIKI_MEDIA_URL = "https://wiki.bristolhackspace.org/_media/"


def md_parse(text: str):
    def make_url(match):
        text = escape(match.group("text"))
        url = match.group("url")
        return f"<a href='{url}' target='_blank' rel='noopener noreferrer'>{text}</a>"
    text = LINK_MD_REGEX.sub(make_url, text)

    def make_img(match):
        link = match.group("link")
        attrs = []
        parts = link.split("?", maxsplit=1)
        if len(parts)==2:
            link = parts[0]
            try:
                width = int(parts[1])
                attrs.append(f"width='{width}rem'")
            except ValueError:
                pass

        wikipath = link.split(":")
        if wikipath[0] == "wiki":
            url = WIKI_MEDIA_URL + "/".join(wikipath[1:])
        else:
            url = url_for("static", filename=link)
        attrs.append(f"src='{url}'")

        attrs = " ".join(attrs)
        return f"<img {attrs}/>"
    text = IMAGE_MD_REGEX.sub(make_img, text)
    return Markup(text)


@bp.route("/quiz/<int:quiz_id>", methods=("GET", "POST"))
@login_required
def index(quiz_id):
    quiz = db.get_or_404(Quiz, quiz_id)

    quiz_data = yaml.load(quiz.questions, Loader=yaml.CLoader)

    class QuizForm(FlaskForm):
        submit_label = "Submit"

    for key, question in quiz_data.items():
            qtype = question["type"]
            label = md_parse(question["label"])
            if qtype == "pick_one":
                choices = list((k, md_parse(v)) for k,v in question["answers"].items())
                answer_validator = Exactly(question["correct_answer"], question.get("incorrect_hint"))
                field = fields.RadioField(label, choices=choices, validators=[InputRequired(), answer_validator])
            elif qtype == "select_all":
                answer_validator = Exactly(set(question["correct_answers"]), question.get("incorrect_hint"))
                choices = list((k, md_parse(v)) for k,v in question["answers"].items())
                field = MultiCheckboxField(label, choices=choices, validators=[answer_validator])
            elif qtype == "yes_no":
                answer_validator = Exactly(question["correct_answer"], question.get("incorrect_hint"))
                field = fields.BooleanField(label, validators=[answer_validator])
            elif qtype == "textbox":
                answer_validator = Exactly(question["correct_answer"], question.get("incorrect_hint"))
                field = fields.StringField(
                    label,
                    validators=[InputRequired(), answer_validator],
                    render_kw={"autocomplete": "off"},
                )
            setattr(QuizForm, key, field)

    quiz_form = QuizForm(request.form, quiz_data=quiz_data)

    if quiz_form.validate_on_submit():
        today=date.today()
        upsert_stmt = insert(Induction).values(
            member_id=g.member.id,
            machine_id=quiz.machine_id,
            state=InductionState.valid,
            inducted_on=today
        ).on_conflict_do_update(
            index_elements=[Induction.member_id, Induction.machine_id],
            set_=dict(
                state=InductionState.valid,
                inducted_on=today
            ),
        )
        db.session.execute(upsert_stmt)
        db.session.commit()
        flash(f"All correct! You should now be able to use the {quiz.machine.name}.")
        return redirect(url_for("general.index"))

    intro_text = md_parse(quiz.intro)

    return render_template("quiz.html", intro_text=intro_text, quiz_form=quiz_form, quiz_title=quiz.title, return_url=url_for("general.index"))