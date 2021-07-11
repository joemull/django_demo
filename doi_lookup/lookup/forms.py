from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class LookUpDOIForm(forms.Form):
    doi = forms.RegexField(
        help_text = 'Valid Digital Object Identifier, either as standalone ID (i.e. starting with "10") or in URL form',
        regex = '(http://|https://)*(doi:|info:doi/|doi\.org/|dx\.doi\.org/)*10\.[0-9.]{4,10}/.*',
        # message = 'Please enter a valid DOI such as 10.3998/ergo.12405314.0007.014 or https://doi.org/10.3998/ergo.12405314.0007.014',
        strip = True,
        label = 'DOI',
    )

    def clean_doi(self):
        data = self.cleaned_data['doi'].lstrip('htps:/doinf.orgx')
        return data
