import requests
import json

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
        article.family_name = message['author'][0]['family']
        if 'given' in message['author'][0]:
            article.given_name = message['author'][0]['given']
        article.save()
        return article

    except:
        return None
