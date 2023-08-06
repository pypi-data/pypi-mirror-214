import pytest
import json
from pubmed_sdk import PubMed

def test_pubmed_search():
    pubmed = PubMed()
    search_term = 'COVID-19'
    results = pubmed.search(search_term)

    # Check that the search returns results
    assert len(results) > 0
    assert 'id_list' in results


def test_pubmed_fetch_details():
    pubmed = PubMed()
    ids = ['33725716']  # Replace with an ID of an actual article
    details = pubmed.fetch_details(ids)

    # Check that details were fetched
    assert len(details) > 0

    # Check that the fetched details have the expected structure
    print(type(details))
    print(type(details))
    assert 'PubmedArticle' in details
    assert 'MedlineCitation' in details['PubmedArticle']
    assert 'Article' in details['PubmedArticle']['MedlineCitation']
    assert 'Abstract' in details['PubmedArticle']['MedlineCitation']['Article']
