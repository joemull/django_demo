from django.test import TestCase
from ..forms import LookUpDOIForm

DIFFERENTLY_FORMATTED_DOIS = [
    '10.1126/science.369.6505.753',
    'https://doi.org/10.1126/science.369.6505.753',
    'http://dx.doi.org/10.1126/science.369.6505.753',
    'doi.org/10.1126/science.369.6505.753',
    'doi:10.1126/science.369.6505.753',
    'info:doi/10.1126/science.369.6505.753',
    '10.5406/jaesteduc.50.1.0062',
    '10.5406/jaesteduc.50.1.0062 ',
    '\n10.5406/jaesteduc.50.1.0062 ',
    '   10.5406/jaesteduc.50.1.0062',
    '10.9999/$',
]

BAD_DOIS = [
    'http://doi.org/10.000/bad.doi',
    '12319aas0d12e1d',
    'dowhat/10.000/3',
    '10.abcd/00',
    '!@*#!@^^!$(!@***@@@***@#!!!!)',
    '{{{{{{{}}}}}}}',
    '""""""\\\\\\"""""',
]

class TestLookupInput(TestCase):

    # Can it handle DOIs from a wide range of publishers?
    # Does it accept good DOIs in lots of forms including ones with whitespace?
    def test_doi_validation(self):
        for doi in DIFFERENTLY_FORMATTED_DOIS:
            form = LookUpDOIForm(data = {'doi' : doi})
            self.assertTrue(form.is_valid())

    # Does it reject bad DOIs?
    def test_reject_bad_dois(self):
        for doi in BAD_DOIS:
            form = LookUpDOIForm(data = {'doi' : doi})
            self.assertFalse(form.is_valid())

    # Does it clean DOIs?
    def test_clean_doi(self):
        for doi in DIFFERENTLY_FORMATTED_DOIS:
            form = LookUpDOIForm(data = {'doi' : doi})
            if form.is_valid():
                for each in ['https','doi','\n','//']:
                    self.assertNotIn(each,form.cleaned_data['doi'])
