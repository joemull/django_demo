import requests
import json

from .models import Article, Contributor

with open('secrets.json') as secrets_file:
    MAILTO = json.loads(secrets_file.read())["MAILTO"]

def get_from_crossref(doi):

    base = f'https://api.crossref.org/works/{doi}'
    parameters = { 'mailto' : MAILTO, }
    response = requests.get(base, params = parameters)
    if response.status_code == 200:
        data = json.loads(response.text)
        if data['status'] == 'ok':
            return parse_crossref_json(data)

    return None

def parse_crossref_json(data):
    try:
        message = data['message']

        article = Article()
        article.doi = message['DOI']
        article.title = message['title'][0]
        if 'license' in message:
            article.license = message['license'][0]['URL']
        if 'abstract' in message:
            article.abstract = message['abstract']
        article.save()

        for author in message['author']:

            if 'ORCID' in author:
                orcid = author['ORCID'].lstrip('htps:/orcid.g')
                if Contributor.objects.filter(orcid__exact=orcid).exists():
                    article.contributors.add(Contributor.objects.get(orcid=orcid))
                    continue

            # if 'email' etc.
            # continue

            contributor = Contributor()
            contributor.family_name = author['family']
            if 'given' in author:
                contributor.given_name = author['given']
            # ADD EMAIL
            if 'ORCID' in author:
                contributor.orcid = author['ORCID'].lstrip('htps:/orcid.g')
            contributor.save()
            article.contributors.add(contributor)

        return article

    except:
        return None
