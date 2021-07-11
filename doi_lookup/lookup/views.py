from django.views import generic
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from .models import Article
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
        if form.is_valid():

            clean_doi = form.cleaned_data['doi']

            try:
                context['article'] = Article.objects.get(doi=clean_doi)
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

    return render(request, 'index.html', context = context)

class ArticleListView(generic.ListView):
    model = Article
    paginate_by = 10

class ArticleDelete(generic.edit.DeleteView):
    model = Article
    success_url = reverse_lazy('articles')
