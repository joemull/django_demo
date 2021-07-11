from django.contrib import admin

from .models import Article, Contributor, Contribution

admin.site.register(Article)
admin.site.register(Contributor)
admin.site.register(Contribution)
