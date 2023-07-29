from wtforms import Field, widgets
from flask import url_for

class SerialField(Field):
    """
    A text field, except all input is coerced to an integer.  Erroneous input
    is ignored and will not be accepted as a value.
    """

    widget = widgets.TextInput()

    def __init__(self, label=None, validators=None, suppress_enter=True, render_kw=None, **kwargs):
        if suppress_enter:
            render_kw = render_kw or {}
            render_kw["data-suppress-enter"] = "1"
        super().__init__(label, validators, render_kw=render_kw, **kwargs)

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data is not None:
            return f'{self.data:x}'
        return ""

    def process_formdata(self, valuelist):
        if not valuelist:
            return

        try:
            self.data = int(valuelist[0], 16)
        except ValueError as exc:
            self.data = None
            raise ValueError(self.gettext("Not a valid serial number.")) from exc

def card_serial_formatter(view, context, model, name):
    if model.card_serial:
        return f"{model.card_serial:x}"
    else:
        return ""

class ViewHelperJsMixin():
    def render(self, template, **kwargs):
        """
        using extra js in render method allow use
        url_for that itself requires an app context
        """
        self.extra_js = [url_for("static", filename="js/helpers.js")]

        return super().render(template, **kwargs)