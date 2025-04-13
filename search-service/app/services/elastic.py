from elasticsearch import Elasticsearch

# Подключение к Elasticsearch
# Если вы используете docker-compose, убедитесь, что имя хоста правильно (например, "elasticsearch")
es = Elasticsearch("http://elasticsearch:9200")

def perform_search(query: str):
    body = {
        "query": {
            "match": {
                "content": {
                    "query": query,
                    "fuzziness": "AUTO"  # можно добавить опцию, если хотите поддерживать неточные совпадения
                }
            }
        }
    }
    try:
        res = es.search(index="documents", body=body)
        hits = res.get("hits", {}).get("hits", [])
        return [hit.get("_source") for hit in hits]
    except Exception as e:
        return {"error": str(e)}
