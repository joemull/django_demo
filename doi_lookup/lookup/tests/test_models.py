from django.test import TestCase

from ..models import *
from .test_harvest import UNCLE
from ..harvest import *

class TestArticleModel(TestCase):
    @classmethod
    def setUpTestData(cls):

        contributor = Contributor.objects.create(
            given_name = 'Bob',
            family_name = 'Du Plessis',
            email = 'bobduplessis@example.com',
            orcid = '0000-0001-5109-3700',
        )

        article = Article.objects.create(
            doi = '10.0000/1',
            title = "Bob's Your Uncle",
            abstract = "And that's that.",
            license = License.objects.create(
                url = 'https://creativecommons.org/licenses/by/4.0/',
            ),
        )

        Contribution.objects.create(
            article = article,
            contributor = contributor
        )

    def test_doi_label(self):
        article = Article.objects.get(doi = '10.0000/1')
        doi_label = article._meta.get_field('doi').verbose_name
        self.assertEqual(doi_label,'DOI')

    def test_contributor_string(self):
        article = Article.objects.get(doi = '10.0000/1')
        contributor = article.contributors.all()[0]
        self.assertEqual(str(contributor),'Du Plessis, Bob')


class TestDelete(TestCase):

    # Does it remove authors when their last article is removed?
    def test_remove_author_when_no_articles_left(self):

        orcid = '0000-0001-5109-3700'
        num_bobs = Contributor.objects.filter(orcid__exact = orcid).count()
        self.assertEqual(num_bobs,0)

        UNCLE['message']['author'][0]['ORCID'] = orcid

        UNCLE['message']['DOI'] = '10.0000/1'
        article1 = parse_crossref_json(UNCLE)
        num_bobs = Contributor.objects.filter(orcid__exact = orcid).count()
        self.assertEqual(num_bobs,1)

        UNCLE['message']['DOI'] = '10.0000/2'
        article2 = parse_crossref_json(UNCLE)
        num_bobs = Contributor.objects.filter(orcid__exact = orcid).count()
        self.assertEqual(num_bobs,1)

        article1.delete()
        num_bobs = Contributor.objects.filter(orcid__exact = orcid).count()
        self.assertEqual(num_bobs,1)

        article2.delete()
        num_bobs = Contributor.objects.filter(orcid__exact = orcid).count()
        self.assertEqual(num_bobs,0)
