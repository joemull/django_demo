from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest, QueryDict
from diskcache import Cache

from .. import views
from ..models import *
from .test_forms import DIFFERENTLY_FORMATTED_DOIS

class TestLookupPage(TestCase):

    # Does it catch duplicate articles and avoid multiple records?
    # Runs only every 12 hours to avoid crowding the API
    def test_doi_validation(self):
        with Cache("testing_cache") as cache:

            if "test_doi_validation" in cache:
                pass
            else:
                cache.set("test_doi_validation", {}, expire = 43200)

                request = HttpRequest()
                request.method = 'POST'

                doi = 'https://doi.org/10.1126/science.369.6505.753'
                request.POST = QueryDict.fromkeys(['doi'], value = doi)
                response = views.index(request)
                self.assertIn(
                    "<p>Article added</p>",
                    str(response.content)
                )

                same_doi = 'http://dx.doi.org/10.1126/science.369.6505.753'
                request.POST = QueryDict.fromkeys(['doi'], value = doi)
                response = views.index(request)
                self.assertIn(
                    "<p>Article already saved to the list</p>",
                    str(response.content)
                )

# The first 5 functions in this test class lean particularly heavily on MDN's Local Library tutorial:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#views
class TestListViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_articles = 13

        contributor = Contributor.objects.create(
            given_name = 'Bob',
            family_name = 'Du Plessis',
            email = 'bobduplessis@example.com',
            orcid = '0000-0001-5109-3700',
        )

        for article_id in range(number_of_articles):
            article = Article.objects.create(
                doi = f'10.0000/{article_id}',
                title = f'Article {article_id}',
            )

            Contribution.objects.create(
                article = article,
                contributor = contributor
            )

        contributor13 = Contributor.objects.create(
            given_name = 'Author13',
            family_name = 'Surname',
        )

        Contribution.objects.create(
            article = article,
            contributor = contributor13
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/lookup/articles/')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lookup/article_list.html')

    def test_lists_all_authors(self):
        response = self.client.get(reverse('articles')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['article_list']), 3)

    # End of near-exact MDN content


    # Does it return filtered list as expected
    def test_filtered_view(self):
        response = self.client.get(reverse('articles') + 'Bob_Du Plessis/')
        self.assertTrue(response.status_code, 200)
        self.assertEqual(len(response.context['article_list']),10)

        response = self.client.get(reverse('articles') + 'Author13_Surname/')
        self.assertTrue(response.status_code, 200)
        self.assertEqual(len(response.context['article_list']),1)

    # Does it handle user-edited URLs gracefully?
    def test_user_edited_url(self):
        response = self.client.get(reverse('articles') + 'Author500_Clark/')
        self.assertTrue(response.status_code, 200)
        self.assertEqual(len(response.context['article_list']),0)
        self.assertIn("Look one up!",str(response.content))
