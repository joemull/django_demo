from django.test import TestCase
from diskcache import Cache
from time import sleep
from datetime import datetime

import json
from ..harvest import *
from ..views import *
from ..models import *

DOIS = [
    '10.1126/science.370.6522.1261',
    '10.1126/science.372.6546.1024',
    '10.2979/jmodelite.38.2.191',
    '10.1002/jmv.25886',
    '10.1186/s12929-020-00695-2',
    '10.2979/jmodelite.34.2.1',
]

BAD_DOIS = [
    '10.0000/bad.bad.doi',
]

UNCLE = {
    "message" : {
        "DOI" : "10.0000/1",
        "title" : [ "Bob's Your Uncle" ],
        "author" : [ { "family" : "Du Plessis", }, ],
    },
}

BAD_ORCIDS = [
    '  https://orcid.org/bobs-your-grea-tuncle',
    'https://orcid.org/0000-0002-1825-0297',
    'https://orcid.org/0080-0001-5109-3700',
]

with open('secrets.json') as secrets_file:
    MAILTO = json.loads(secrets_file.read())["MAILTO"]

class TestCrossref(TestCase):

    # Does it get things from the API but only store 200 responses?
    # This only runs if haven't run this test for 12 hours to avoid crowding the API
    def test_crossref_works(self):

        with Cache('testing_cache') as cache:
            for doi in DOIS:
                if doi in cache:
                    response = cache[doi]
                    self.assertTrue(True)

                else:

                    article = get_from_crossref(doi)
                    self.assertGreater(len(article.title),1)
                    article.delete()

                    sleep(3)

                    response = requests.get(
                        f'https://api.crossref.org/works/{doi}',
                        params = { 'mailto' : MAILTO}
                    )
                    cache.set(doi, response, expire = 43200)


    # Does it reject responses not OK from Crossref?
    # Only runs every 12 hours to avoid crowding the API
    def test_rejects_crossref_status_not_ok(self):
        with Cache('testing_cache') as cache:
            for doi in BAD_DOIS:
                if doi in cache:
                    response = cache[doi]
                    self.assertTrue(True)

                else:
                    article = get_from_crossref(doi)
                    self.assertEqual(article,None)

                    sleep(3)

                    response = requests.get(
                        f'https://api.crossref.org/works/{doi}',
                        params = { 'mailto' : MAILTO}
                    )
                    cache.set(doi, response, expire = 43200)

    # Can it handle a sparse record?
    def test_handle_sparse_record(self):
        UNCLE['message']['DOI'] = '10.0000/1'
        sparse_article = parse_crossref_json(UNCLE)
        self.assertEqual(sparse_article.title,"Bob's Your Uncle")
        sparse_article.delete()

class TestORCID(TestCase):

    # Does it handle multiple formats of ORCID including ones with whitespace?
    # Does it properly link to contributors already in the database?
    # Does it clean ORCIDs?
    def test_orcid_validation_and_cleaning(self):

        UNCLE['message']['DOI'] = '10.0000/1'
        orcid = 'https://orcid.org/0000-0001-5109-3700'
        UNCLE['message']['author'][0]['ORCID'] = orcid
        article1 = parse_crossref_json(UNCLE)
        bob_records = Contributor.objects.filter(family_name__exact='Du Plessis')
        self.assertEqual(bob_records.count(),1)

        UNCLE['message']['DOI'] = '10.0000/2'
        same_orcid = '  orcid.org/0000-0001-5109-3700/     \n'
        UNCLE['message']['author'][0]['ORCID'] = same_orcid
        article2 = parse_crossref_json(UNCLE)
        bob_records = Contributor.objects.filter(family_name__exact='Du Plessis')
        self.assertEqual(bob_records.count(),1)

        UNCLE['message']['DOI'] = '10.0000/3'
        still_same_orcid = '  orcid.org/0000000151093700/     \n'
        UNCLE['message']['author'][0]['ORCID'] = still_same_orcid
        article3 = parse_crossref_json(UNCLE)
        bob_records = Contributor.objects.filter(family_name__exact='Du Plessis')
        self.assertEqual(bob_records.count(),1)

        UNCLE['message']['author'][0].pop('ORCID')
        UNCLE['message']['DOI'] = '10.0000/1'
        article1.delete()
        article2.delete()
        article3.delete()

    # Does it ignore bad ORCIDs?
    def test_reject_bad_orcids(self):
        for bad_orcid in BAD_ORCIDS:

            UNCLE['message']['DOI'] = '10.0000/1'
            UNCLE['message']['author'][0]['ORCID'] = bad_orcid
            article = parse_crossref_json(UNCLE)
            bob_records = Contributor.objects.filter(family_name__exact='Du Plessis')
            self.assertEqual(bob_records[0].orcid,None)

            UNCLE['message']['author'][0].pop('ORCID')
            article.delete()


class TestLicense(TestCase):

    # Can it handle whitespace in License URL fields?
    # Does it catch duplicate licenses and avoid multiple records?
    # Does it properly link to existing license records?
    def test_catch_duplicate_licenses(self):

        UNCLE['message']['DOI'] = '10.0000/1'
        license = 'https://creativecommons.org/licenses/by/4.0/'
        UNCLE['message']['license'] = [{'URL' : license}]
        article1 = parse_crossref_json(UNCLE)

        UNCLE['message']['DOI'] = '10.0000/2'
        same_license = '    https://creativecommons.org/licenses/by/4.0/\n '
        UNCLE['message']['license'][0]['URL'] = same_license
        article2 = parse_crossref_json(UNCLE)

        articles = Article.objects.filter(title__exact = "Bob's Your Uncle")
        self.assertEqual(
            articles[0].license.pk,
            articles[1].license.pk
        )

        UNCLE['message'].pop('license')
        UNCLE['message']['DOI'] = '10.0000/1'
        article1.delete()
        article2.delete()
