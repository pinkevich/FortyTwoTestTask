from django import forms
from django.templatetags.static import static


class DatePickerWidget(forms.DateInput):
    """
    Bootstrap-datetimepicker widget for DateField, use:
    ...
    date = forms.DateField(widget=DatePickerWidget)
    ...
    Note:
        must be connected jQuery and bootstrap.min.css
        check that the files in static
    """

    @property
    def media(self):
        css = {'all': ('css/bootstrap-datetimepicker.min.css',)}
        js = ['moment.min.js', 'bootstrap.min.js',
              'bootstrap-datetimepicker.min.js', 'datepicker.js']
        return forms.Media(
            css=css,
            js=[static('js/{0}'.format(path)) for path in js],
        )

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'DatePickerWidget'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(DatePickerWidget, self).__init__(attrs=final_attrs,
                                               format=format)
