from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from .models import Article, Contributor
from .forms import LookUpDOIForm
from .harvest import get_from_crossref

def index(request):
    """View for landing page with DOI lookup form"""

    context = {
        'message' : None,
        'article' : None,
        'form' : LookUpDOIForm(),
    }

    if request.method == 'POST':

        form = LookUpDOIForm(request.POST)
        context = process_lookup_form(form, context)

    return render(request, 'index.html', context = context)

def process_lookup_form(form, context):

    if form.is_valid():

        clean_doi = form.cleaned_data['doi']

        try:
            context['article'] = Article.objects.get(doi = clean_doi)
            context['message'] = 'Article already saved to the list'

        except:
            article = get_from_crossref(clean_doi)

            if article != None:
                context['article'] = article
                context['message'] = 'Article added'
            else:
                context['message'] = 'Article not found'

    else:
        context['message'] = 'Oops, something went wrong'
        context['form'] = form

    return context

class ArticleListView(generic.ListView):
    model = Article
    paginate_by = 10

class AuthorFilteredArticleListView(ArticleListView):
    def get_queryset(self):
        if 'given_name' in self.kwargs:
            qs = Article.objects.filter(
                contributors__given_name = self.kwargs['given_name'],
                contributors__family_name = self.kwargs['family_name'],
            )
        else:
            qs = Article.objects.filter(
                contributors__family_name = self.kwargs['family_name']
            )
        return qs

    # Credit: https://stackoverflow.com/questions/29598341/extra-context-in-django-generic-listview
    def get_context_data(self,**kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        if 'given_name' in self.kwargs:
            context['query_contributor'] = f"{self.kwargs['given_name']} {self.kwargs['family_name']}"
        else:
            context['query_contributor'] = f"{self.kwargs['family_name']}"
        return context

class ArticleDelete(generic.edit.DeleteView):
    model = Article
    success_url = reverse_lazy('articles')
