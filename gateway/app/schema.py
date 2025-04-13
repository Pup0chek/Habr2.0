import strawberry
import requests

@strawberry.type
class SearchResultItem:
    id: int
    title: str
    content: str

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, World!"

    @strawberry.field
    def lol(self) -> str:
        return "Hello, lol!"

    @strawberry.field
    def search(self, q: str) -> list[SearchResultItem]:
        """
        Выполняет поиск по переданному запросу.
        Резолвер делает GET-запрос к сервису поиска.
        """
        url = "http://search-service:8001/search"
        params = {"q": q}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            results_data = data.get("results", [])
            items = []
            for r in results_data:
                item = SearchResultItem(
                    id=r.get("id", 0),
                    title=r.get("title", ""),
                    content=r.get("content", "")
                )
                items.append(item)
            return items
        except Exception as e:
            print("Ошибка в резолвере search:", e)
            return []

schema = strawberry.Schema(query=Query)
