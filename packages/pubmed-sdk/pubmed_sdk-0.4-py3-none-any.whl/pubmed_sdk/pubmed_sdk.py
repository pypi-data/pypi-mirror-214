import json
from xml.etree import ElementTree

import xmltodict
import requests


def convert_xml_to_dict(xml_string):
    xml_dict = xmltodict.parse(xml_string)
    json_data = json.dumps(xml_dict)
    data = json.loads(json_data)
    return data

class PubMed:
    BASE_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

    def __init__(self, db='pubmed'):
        self.db = db

    def search(self, term, use_history=False):
        eutil = 'esearch.fcgi?'
        term_param = f'&term={term.replace(" ", "+")}'
        use_history_param = f'&usehistory={"y" if use_history else "n"}'
        search_url = f'{self.BASE_URL}{eutil}db={self.db}{term_param}{use_history_param}'
        
        response = requests.get(search_url)
        response_xml = ElementTree.fromstring(response.content)

        return self._parse_search_results(response_xml)

    def fetch_details(self, id_list):
        id_str = ','.join(str(id) for id in id_list)
        eutil = 'efetch.fcgi?'
        fetch_url = f'{self.BASE_URL}{eutil}db={self.db}&id={id_str}'

        response = requests.get(fetch_url)
        data = convert_xml_to_dict(response.content.decode()).get('PubmedArticleSet')
        return data


    def _parse_search_results(self, xml):
        result = {
            'count': xml.find('Count').text,
            'ret_max': xml.find('RetMax').text,
            'ret_start': xml.find('RetStart').text,
            'id_list': [id_node.text for id_node in xml.find('IdList')],
        }

        webenv_node = xml.find('WebEnv')
        if webenv_node is not None:
            result['webenv'] = webenv_node.text

        query_key_node = xml.find('QueryKey')
        if query_key_node is not None:
            result['query_key'] = query_key_node.text

        return result

    def _parse_fetch_results(self, xml):
        articles = []
        for article_node in xml.findall('PubmedArticle'):
            article = {}

            medline_citation_node = article_node.find('MedlineCitation')
            if medline_citation_node is not None:
                article['pmid'] = medline_citation_node.find('PMID').text

                article_meta_node = medline_citation_node.find('Article')
                if article_meta_node is not None:
                    article['title'] = article_meta_node.find('ArticleTitle').text

                    abstract_node = article_meta_node.find('Abstract')
                    if abstract_node is not None:
                        article['abstract'] = abstract_node.find('AbstractText').text

                    authors_node = article_meta_node.find('AuthorList')
                    if authors_node is not None:
                        article['authors'] = [
                            {
                                'last_name': author_node.find('LastName').text,
                                'fore_name': author_node.find('ForeName').text,
                                'initials': author_node.find('Initials').text,
                            }
                            for author_node in authors_node.findall('Author')
                        ]

            articles.append(article)

        return articles
