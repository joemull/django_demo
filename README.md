# DOI Lookup Django Demo

## Description
This app lets you look up articles by their DOIs and save them to a list. When you enter a DOI, it validates the input with regular expressions and checks if the DOI is already recorded in the database. If the DOI is new, the app talks to the Crossref API with `requests` and saves resulting data to three models in a SQLite database:

1. Article (DOI, title, abstract)
2. Contributor (given name, family name, ORCID)
3. License (url)

For each contributor, if there's an ORCID available, the app checks if that Contributor already exists in the database in order to avoid creating duplicate contributor records. It does the same with License URLs. Both DOIs and ORCIDs are validated and shortened to their basic forms before being input into the database.

You can view a list of all articles saved, sorted by title, and you can page through the list if more than ten articles are saved. You can also click on author names in order to view a list of articles by that author. This also works for articles whose authors are only listed by last name (e.g. 10.2979/jmodelite.38.2.191).

You can delete articles from the list. Contributors are also removed when their associated article is deleted, but not if they are also the author of a different article in the list. The relationship between articles and contributors is managed through a many-to-many relationship, including a receiver that removes contributors when their last associated article is removed from the database.

I drew on MDN's [Local Library Django Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django) for some of the structure and design sense of the app. Several other creators are credited in comments as well. I also made use of one of my favorite libraries for API work, [`diskcache`](https://pypi.org/project/diskcache/), to be nicer to the Crossref API in the unit tests.

# Running the app
1. Make sure you have a compatible version of Python installed (tested on 3.7.8).
2. Clone the repository or download the files.
3. Install the app's dependencies (`django` 3.1, `requests`, and `diskcache` for testing) using [`pip`](https://pip.pypa.io/en/stable/). Best to create and activate a virtual environment with something like [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/) and run `pip install -r requirements.txt` to install them all at once.
4. In `doi_lookup`, rename `sample_secrets.json` as `secrets.json` and enter a development key of your choosing for `SECRET_KEY` and your email address for `MAILTO` as a courtesy to Crossref.
5. Navigate to the same directory as `python manage.py`, run the app with `python manage.py runserver`, and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view in your browser.

# Testing
There are selective unit tests, with better coverage for things more likely to break, such as the functions that call the Crossref API.

Note that some of the tests get live data from the API and use a sleep timer, so the first time the tests run it will take about 15-20 seconds. After the first test run this info is cached for 12 hours.

To run the tests, navigate to the same directory as `manage.py` and use `python manage.py test`.

# Viewing the admin interface
A basic admin view is available at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
