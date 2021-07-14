# OLH Django Demo

# Description
This app allows users to look up articles by their DOIs and save them to a list. When the user enters a DOI, it validates the input with regex and checks if the DOI is already recorded in the database. If not found, it sends the DOI to the Crossref API with `requests` and saves resulting data to three models:

1. Article (DOI, title, abstract)
2. Contributor (given name, family name, ORCID)
3. License (url)

[TESTING OF API]

For each contributor, if there's an ORCID available, the app checks if that Contributor already exists in the database in order to avoid creating duplicate records. It does the same with License URLs. Both DOIs and ORCIDs are validated and shortened to their basic forms before being input into the database.

Users can view a list of all articles saved [SORTED?], and they can page through the list if more than ten articles are saved. They can delete articles from the list. The relationship between articles and contributors is managed through a many-to-many relationship, including a receiver that removes contributors when their last associated article is removed.

Users can also click on author names in order to view a list of articles by that author. [SUPPORT FOR NO FIRST NAMES?]
