
from wtforms import fields, validators
from flask import flash, redirect, request
from flask_admin import form, Admin, BaseView, expose
from flask_admin.helpers import get_redirect_target, validate_form_on_submit

class FirmwareUpdateForm(form.BaseForm):
    upload = fields.FileField('File to upload')

    def __init__(self, *args, **kwargs):
        super(FirmwareUpdateForm, self).__init__(*args, **kwargs)
        self.admin = kwargs['admin']

    def validate_upload(self, field):
        if not self.upload.data:
            raise validators.ValidationError('File required.')

class FirmwareUpdateView(BaseView):

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = self.upload_form()
        return_url = get_redirect_target() or self.get_url('.index')

        if validate_form_on_submit(form):
            data = request.files[form.upload.name].read()
            with open("/run/hackspace-mgmt/firmware_update.bin", "wb") as fh:
                fh.write(data)
            flash(f'Successfully saved file: {form.upload.data.filename}', 'success')
            return redirect(return_url)

        return self.render('admin/firmware_update.html', return_url=return_url, form=form)

    def upload_form(self):
        if request.form:
            # Workaround for allowing both CSRF token + FileField to be submitted
            # https://bitbucket.org/danjac/flask-wtf/issue/12/fieldlist-filefield-does-not-follow
            formdata = request.form.copy()  # as request.form is immutable
            formdata.update(request.files)

            # admin=self allows the form to use self.is_file_allowed
            return FirmwareUpdateForm(formdata, admin=self)
        elif request.files:
            return FirmwareUpdateForm(request.files, admin=self)
        else:
            return FirmwareUpdateForm(admin=self)

def create_views(admin: Admin):
    admin.add_view(FirmwareUpdateView("Firmware Update", endpoint="firmware_update", category="Access Control"))