from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from hackspace_mgmt.audit import create_audit_log
from hackspace_mgmt.models import QuizCompletion, db, Quiz
from hackspace_mgmt.forms import ViewHelperJsMixin
from wtforms.fields import TextAreaField


class QuizView(ViewHelperJsMixin, ModelView):
    form_overrides = {
        "questions": TextAreaField,
        "intro": TextAreaField
    }

class QuizCompletionView(ViewHelperJsMixin, ModelView):
    column_list = ('member', 'quiz', 'completed_on')
    can_create=False
    can_edit=False

    def on_model_delete(self, model: QuizCompletion):
        # Don't commit the log. This will happen when the view deletes the record.
        create_audit_log(
            "quiz",
            "revoke",
            data={
                "quiz_id": model.quiz_id
            },
            member_id=model.member_id,
            commit=False
        )


def create_views(admin: Admin):
    admin.add_view(QuizView(Quiz, db.session, endpoint="quiz_view", category="Access Control"))
    admin.add_view(QuizCompletionView(QuizCompletion, db.session, endpoint="quiz_completion_view", category="Access Control"))