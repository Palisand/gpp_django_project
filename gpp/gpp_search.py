from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()


def run_query(search, agencies_selected=None, categories_selected=None, types_selected=None, start=0, num_results=10):

    results = []

    if search:

        query_list = [
            {
                "multi_match": {
                    "query": search,
                    "fields": ["title", "description", "file"],
                    "type": "best_fields",
                    "cutoff_frequency": 0.0001
                },
            },
        ]

        if agencies_selected:
            query_list.append({"in": {"agency": agencies_selected, }, })

        if categories_selected:
            query_list.append({"in": {"category": categories_selected, }, })

        if types_selected:
            query_list.append({"in": {"type": types_selected, }, })

        results = es.search(index='publications2', body={
                "from": start, "size": num_results,
                "query": {
                    "bool": {
                        "must": query_list
                    }
                }
            }
        )

    return results['hits']['hits']


def sort_query():
    pass