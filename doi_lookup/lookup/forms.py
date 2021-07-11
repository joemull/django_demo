from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class LookUpDOIForm(forms.Form):
    doi = forms.RegexField(
        help_text = 'Enter a DOI by itself (e.g. 10.1145/2892557) or in URL form (e.g. https://doi.org/10.1145/2892557)',
        regex = '(http://|https://)*(doi:|info:doi/|doi\.org/|dx\.doi\.org/)*10\.[0-9.]{4,10}/.*',
        strip = True,
        label = 'DOI',
    )

    def clean_doi(self):
        data = self.cleaned_data['doi'].lstrip('htps:/doinf.orgx')
        return data
