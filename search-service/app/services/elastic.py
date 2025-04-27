from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, RequestError
from typing import Optional

es = None
try:
    es = Elasticsearch("http://elasticsearch:9200")
    if not es.ping():
        raise ConnectionError("Could not connect to Elasticsearch")
except ConnectionError as e:
    print(f"Elasticsearch connection error: {e}")
    es = None

def perform_search(query: str):
    if es is None:
        raise ConnectionError("Elasticsearch connection is not established")
    
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "content", "author"],
                "fuzziness": "AUTO"
            }
        }
    }
    try:
        res = es.search(index="documents", body=body)
        return [
            {
                "_id": hit["_id"],
                **hit["_source"]
            }
            for hit in res["hits"]["hits"]
        ]
    except Exception as e:
        print(f"Search error: {str(e)}")
        raise

def create_document(title: str, content: str, author: Optional[str] = None):
    if es is None:
        raise ConnectionError("Elasticsearch connection is not established")
    
    doc = {
        "title": title,
        "content": content,
        "author": author
    }
    
    try:
        res = es.index(index="documents", document=doc)
        return {
            "_id": res["_id"],
            **doc
        }
    except RequestError as e:
        print(f"Document creation error: {str(e)}")
        raise