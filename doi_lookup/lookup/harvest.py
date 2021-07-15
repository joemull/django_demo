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
        license_url = message['license'][0]['URL'].strip(string.whitespace)
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
            orcid = get_clean_orcid(author['ORCID'])
            if orcid != None:
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
            orcid = get_clean_orcid(author['ORCID'])
            if orcid != None:
                contributor.orcid = orcid
        contributor.save()
        article.contributors.add(contributor)

    return article

    # except:
    #     return None

def get_clean_orcid(orcid_messy):
    hyphenated = re.search('([0-9]{4,4}\-){3,3}[0-9X]{4,4}',orcid_messy)
    sixteen_digits = re.search('[0-9X]{16,16}',orcid_messy)

    if hyphenated != None:
        s16 = hyphenated.group().replace("-","")
    elif sixteen_digits != None:
        s16 = sixteen_digits.group()
    else:
        return None

    if check_digit_matches(s16):
        return f'{s16[0:4]}-{s16[4:8]}-{s16[8:12]}-{s16[12:16]}'
    else:
        return None

# Credit https://github.com/tjwds/generate-orcid-checksum#generatecheckdigit
# Reference https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
def check_digit_matches(orcid):
    orcid_string = str(orcid)
    base_digits = orcid_string[:-1]
    total = 0
    for i in base_digits:
        total = (total + int(i)) * 2
    remainder = total % 11
    check_digit = (12 - remainder) % 11
    if check_digit == 10:
        check_digit = "X"
    if str(check_digit) == orcid_string[-1]:
        return True
    else:
        return False
