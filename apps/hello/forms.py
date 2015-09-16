from django import forms

from .models import Bio


class BioEditForm(forms.ModelForm):

    class Meta:
        model = Bio
