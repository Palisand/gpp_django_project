import os
import base64
import time
from elasticsearch import Elasticsearch
es = Elasticsearch()

INDEX = 'publications2'
DOCTYPE = 'document'


def index():
    es.indices.delete(index=INDEX, ignore=[400, 404])
    es.indices.create(index=INDEX, body={
        "index": {
            "analysis": {
                "analyzer": {
                    "gpp_analyzer": {
                        "type": "snowball",
                        "language": "English"
                    }
                }
            }
        }
    })

    index_time_start = time.clock()

    es.indices.put_mapping(index=INDEX, doc_type=DOCTYPE, body={
        DOCTYPE: {
            'properties': {
                'id':             {'type': 'integer'},
                'title':          {'type': 'string', 'analyzer': 'gpp_analyzer', 'index': 'analyzed'},
                'description':    {'type': 'string', 'analyzer': 'gpp_analyzer', 'index': 'analyzed'},
                'date_created':   {'type': 'date'},
                'common_id':      {'type': 'integer'},
                'section_id':     {'type': 'integer'},
                'pub_or_foil':    {'type': 'string', 'index': 'no'},
                'agency':         {'type': 'string', 'index': 'not_analyzed'},
                'category':       {'type': 'string', 'index': 'not_analyzed'},
                'type':           {'type': 'string', 'index': 'not_analyzed'},
                'url':            {'type': 'string', 'index': 'no'},
                # 'file':           {
                #     'type': 'attachment',
                #     # 'analyzer': 'gpp_analyzer',
                #     'index': 'no', # still doesn't work, what the hell?!
                #     # 'fields': {
                #     #     'keywords': {'store': 'yes'}
                #     # }
                # }
            }
        }
    })

    docs = Document.objects.all()

    # docs = Document.objects.filter(id=1)
    # file = open('/Users/Palisand/Documents/DORIS/misc_scripts/test', 'r')
    # lines = file.readlines()
    # b64encoded = ''
    # for line in lines:
    #     b64encoded += line.strip()

    for doc in docs:
        es.index(index=INDEX, doc_type=DOCTYPE, body={
            "id":           doc.id,
            "title":        doc.title,
            "description":  doc.description,
            "date_created": doc.date_created,
            "common_id":    doc.common_id,
            "section_id":   doc.section_id,
            "pub_or_foil":  doc.pub_or_foil,
            "agency":       doc.agency,
            "category":     doc.category,
            "type":         doc.type,
            "url":          doc.url,
            # "file":         b64encoded
        })

    index_time_elapsed = time.clock() - index_time_start
    print "Completed in: %f seconds" %index_time_elapsed


if __name__ == "__main__":
    print "Indexing database..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gpp_django_project.settings') #look up why!!!
    from gpp.models import Document
    index()