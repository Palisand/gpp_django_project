from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()


def run_query(query, agencies_selected=None, categories_selected=None, types_selected=None, sort_method='Relevance', start=0, size=10):

    results = []
    match_list = []

    if query:

        match_list = [
            {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description", "agency", "category", "type"], # "file"],
                    "type": "best_fields",
                    "cutoff_frequency": 0.0001
                },
            },
        ]

    filter_update(match_list, agencies_selected, categories_selected, types_selected)

    raw_results = es.search(index='publications2', body={
            "from": start,
            "size": size,
            "query": {
                "bool": {
                    "must": match_list
                }
            },
            "highlight": {
                "pre_tags": ["<strong>"],
                "post_tags": ["</strong>"],
                "fields": {
                    "_all": {}
                }
            }
        }
    )

    rank = int(start)
    for result in raw_results['hits']['hits']:
        rank += 1
        result[u'_source'][u'rank'] = rank
        results.append(result['_source'])

    total = raw_results['hits']['total']

    return results, total


def sort_query():
    pass


def filter_update(match_list, agencies, categories, types):

    if agencies:
        match_list.append({"in": {"agency": agencies, }, })

    if categories:
        match_list.append({"in": {"category": categories, }, })

    if types:
        match_list.append({"in": {"type": types, }, })