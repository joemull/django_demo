import requests
import json
import string
import re

from .models import Article, Contributor, License

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
    # try:
    message = data['message']

    article = Article()
    article.doi = message['DOI']
    article.title = message['title'][0]
    if 'license' in message:
        license_url = message['license'][0]['URL']
        if License.objects.filter(url__exact = license_url).exists():
            article.license = License.objects.get(url = license_url)
        else:
            license = License(url = license_url)
            license.save()
            article.license = license

    if 'abstract' in message:
        article.abstract = message['abstract']
    article.save()

    for author in message['author']:

        if 'ORCID' in author:
            orcid_url = author['ORCID']
            m = re.search('([0-9]{4,4}\-){3,3}[0-9]{4,4}',orcid_url)
            orcid = m.group()
            print(orcid)
            if Contributor.objects.filter(orcid__exact=orcid).exists():
                article.contributors.add(Contributor.objects.get(orcid=orcid))
                continue

        # if 'email' check for existing contributor and link if found

        contributor = Contributor()
        contributor.family_name = author['family']
        if 'given' in author:
            contributor.given_name = author['given']
        # ADD EMAIL for new contributor records
        if 'ORCID' in author:
            contributor.orcid = author['ORCID'].lstrip('htps:/orcid.g')
        contributor.save()
        article.contributors.add(contributor)

    return article

    # except:
    #     return None
