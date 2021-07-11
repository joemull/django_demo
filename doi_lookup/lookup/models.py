from django.db import models

class Article(models.Model):
    """A journal article model"""

    # Fields
    doi = models.CharField(
        help_text = 'The Digital Object Identifier (e.g. 10.3998/ergo.12405314.0002.002)',
        max_length = 255,
        verbose_name = 'DOI',
    )

    title = models.CharField(
        help_text = 'The full title of the article including its subtitle',
        max_length = 255,
    )

    abstract = models.TextField(
        help_text = 'The abstract of the article',
        max_length = 2000,
        null = True,
        blank = True,
    )

    license = models.URLField(
        help_text = 'The full web address for a license page such as a https://creativecommons.org/licenses/by/4.0/',
        null = True,
        blank = True,
    )

    # Author fields for MVP
    given_name = models.CharField(
        help_text = 'First or given name of person (leave blank for organizations)',
        max_length = 100,
        null = True,
        blank = True,
    )

    family_name = models.CharField(
        help_text = 'Last or family name of person, or name of organization as contributor',
        max_length = 100,
    )

    email = models.EmailField(
        null = True,
        blank = True,
    )

    # Metadata
    ordering = ['title']

    # Methods
    def __str__(self):
        return self.title


# # Contributor class for bonus
# class Contributor(models.Model):
#
#     # Fields
#
#     # Metadata
#     ordering = ['family_name','given_name']
#
#     # Methods
#     def __str__(self):
#         if self.given_name != '':
#             return f'{self.family_name}, {self.given_name}'
#         else:
#             return self.family_name
