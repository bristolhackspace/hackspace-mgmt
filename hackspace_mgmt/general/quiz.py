from flask import Blueprint, flash, redirect, render_template, url_for, request, g
from flask_wtf import FlaskForm
from markupsafe import Markup, escape
from wtforms import fields, widgets, ValidationError
from wtforms.validators import InputRequired
from sqlalchemy.dialects.postgresql import insert
import yaml
import logging
import re
from datetime import datetime, timezone

from hackspace_mgmt.models import Machine, QuizCompletion, db, Quiz, Member, Induction, InductionState, LegacyMachineAuth
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

    machine_id = request.args.get("machine_id")
    if machine_id is not None:
        return_url = url_for("induction.machine", machine_id=machine_id)
    else:
        return_url = url_for("general.index")

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
        now=datetime.now(timezone.utc)
        upsert_stmt = insert(QuizCompletion).values(
            member_id=g.member.id,
            quiz_id=quiz.id,
            completed_on=now
        ).on_conflict_do_update(
            index_elements=[QuizCompletion.quiz_id, QuizCompletion.member_id],
            set_=dict(
                completed_on=now
            ),
        )
        db.session.execute(upsert_stmt)
        db.session.commit()
        correct_msg = f"All correct! "

        machine = None
        if machine_id is not None:
            machine = db.session.get(Machine, machine_id)
        if machine:
            if machine.is_member_inducted(g.member):
                if machine.legacy_auth == LegacyMachineAuth.padlock:
                    correct_msg += f"The padlock code for the {machine.name} is {machine.legacy_password}."
                elif machine.legacy_auth == LegacyMachineAuth.password:
                    correct_msg += f"The password for the {machine.name} is \"{machine.legacy_password}\"."
                else:
                    correct_msg += f"You should now be able to use the {machine.name}."
            else:
                correct_msg += "You'll need to complete further training first however."
        flash(correct_msg)
        return redirect(return_url)

    intro_text = md_parse(quiz.intro)



    return render_template("quiz.html", intro_text=intro_text, quiz_form=quiz_form, quiz_title=quiz.title, return_url=return_url)