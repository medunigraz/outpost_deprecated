from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class TokenForm(forms.ModelForm):
    compliance = forms.BooleanField(
        required=True,
        label=_('Data protection agreement')
    )

    class Meta:
        model = models.Token
        fields = (
            'purpose',
            'lifetime',
        )
