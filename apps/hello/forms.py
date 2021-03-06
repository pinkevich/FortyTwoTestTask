from datetime import date

from django import forms

from .models import Bio
from .widgets import DatePickerWidget


class BioEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=DatePickerWidget)

    class Meta:
        model = Bio

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        less_year = 1930
        if date_of_birth.year < less_year:
            raise forms.ValidationError(
                'Year greater than or equal to {}'.format(less_year)
            )
        year = date.today().year
        if date_of_birth.year > year:
            raise forms.ValidationError(
                'Year less than or equal to {}'.format(year)
            )
        return date_of_birth
