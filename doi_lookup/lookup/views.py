from django.shortcuts import render
from django.views import generic

from .models import Article

def index(request):
    """View for landing page with DOI lookup form"""
    context = {}

    return render(request, 'index.html', context = context)

class ArticleListView(generic.ListView):
    model = Article
