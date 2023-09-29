from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from hackspace_mgmt.models import db, Quiz, Machine
from hackspace_mgmt.forms import ViewHelperJsMixin
from wtforms.fields import TextAreaField


class QuizView(ViewHelperJsMixin, ModelView):
    form_ajax_refs = {
        'machine': QueryAjaxModelLoader('machine', db.session, Machine, fields=['name'], page_size=10, placeholder="Please select machine")
    }

    form_overrides = {
        "questions": TextAreaField
    }



def create_views(admin: Admin):
    admin.add_view(QuizView(Quiz, db.session, endpoint="quiz_view", category="Access Control"))