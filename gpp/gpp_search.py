from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()


def run_query(query, agencies_selected=None, categories_selected=None, types_selected=None, start=0, size=10, sort_method='relevance'):

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

    sort = set_sort(sort_method)

    raw_results = es.search(index='publications2', body={
        "from": start,
        "size": size,
        "sort": sort,
        "query": {
            "bool": {
                "must": match_list
            }
        },
        "highlight": {
            "pre_tags": ["<strong>"],
            "post_tags": ["</strong>"],
            "fields": {
                "title": {"number_of_fragments": 0},
                "description": {"number_of_fragments": 0},
                "agency": {},
                "category": {},
                "type": {}
            }
        }
    })

    results = es_process(raw_results, start)
    total = raw_results['hits']['total']

    return results, total


def filter_update(match_list, agencies, categories, types):

    if agencies:
        match_list.append({"in": {"agency": agencies, }, })

    if categories:
        match_list.append({"in": {"category": categories, }, })

    if types:
        match_list.append({"in": {"type": types, }, })


def set_sort(sort_method):

    sort_by = {
        "relevance": ["_score"],
        "newest": [{"date_created": "desc"}],
        "oldest": [{"date_created": "asc"}],
        "title-asc": [{"title.raw": "asc"}],
        "title-desc": [{"title.raw": "desc"}],
        "agency-asc": [{"agency": "asc"}],
        "agency-desc": [{"agency": "desc"}],
    }

    return sort_by[sort_method]


def es_process(es_search, start):

    results = []

    rank = int(start)
    for result in es_search['hits']['hits']:
        rank += 1
        result[u'_source'][u'rank'] = rank
        if u'highlight' in result:
            highlight(result, u'title')
            highlight(result, u'description')
            highlight(result, u'agency')
            highlight(result, u'category')
            highlight(result, u'type')
        result[u'_source'][u'score'] = result[u'_score']
        results.append(result['_source'])

    return results


def highlight(result, field):
    if field in result[u'highlight'].keys():
        result[u'_source'][field] = result[u'highlight'][field][0]
