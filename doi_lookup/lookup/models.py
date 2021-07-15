from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

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

    license = models.ForeignKey(
        'License',
        on_delete = models.SET_NULL,
        null = True,
        blank = True
    )

    contributors = models.ManyToManyField(
        'Contributor',
        through='Contribution',
        through_fields=('article', 'contributor'),
        help_text = 'A contributor to the article',
        blank = True,
    )

    # Metadata
    class Meta:
        ordering = ['title']

    # Methods
    def __str__(self):
        return self.title

    # Delete contributor when authored article is deleted if they don't have any other articles in the database
    @receiver(post_delete, sender = 'lookup.Contribution')
    def remove_orphaned_contributor(**kwargs):
        contributor = kwargs['instance'].contributor
        if not Contribution.objects.filter(contributor=contributor.pk).exists():
            contributor.delete()

# Contributor class for bonus
class Contributor(models.Model):

    # Fields
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

    orcid = models.CharField(
        help_text = 'The ORCID identifier (e.g. 0000-0003-3230-6090)',
        max_length = 255,
        null = True,
        blank = True,
        verbose_name = 'ORCID',
    )

    # Methods
    def __str__(self):
        if self.given_name != '':
            return f'{self.family_name}, {self.given_name}'
        else:
            return self.family_name

class Contribution(models.Model):

    # Fields
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    contributor = models.ForeignKey('Contributor', on_delete=models.CASCADE)

class License(models.Model):
    url = models.URLField(
        help_text = 'The full web address for a license page such as a https://creativecommons.org/licenses/by/4.0/',
        null = True,
        blank = True,
    )
