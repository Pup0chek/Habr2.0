import strawberry
from typing import Optional
import requests
from json import JSONDecodeError

@strawberry.type
class Document:
    id: str
    title: str
    content: str
    author: Optional[str] = None

@strawberry.type
class Query:
    @strawberry.field
    def search(self, q: str) -> list[Document]:
        try:
            response = requests.get(
                f"http://search-service:8001/search?q={q}",
                timeout=5
            )
            
            # Проверяем успешность запроса
            response.raise_for_status()
            
            results = response.json()
            
            if not isinstance(results, list):
                print(f"Unexpected response format: {results}")
                return []
                
            return [
                Document(
                    id=str(result.get("_id", "")),
                    title=result.get("title", ""),
                    content=result.get("content", ""),
                    author=result.get("author")
                )
                for result in results
            ]
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return []
        except JSONDecodeError as e:
            print(f"Invalid JSON response: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return []

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_document(self, title: str, content: str, author: Optional[str] = None) -> Document:
        try:
            # Пример реального запроса к сервису:
            response = requests.post(
                "http://search-service:8001/documents",
                json={"title": title, "content": content, "author": author},
                timeout=5
            )
            response.raise_for_status()
            result = response.json()
            
            return Document(
                id=str(result["_id"]),
                title=result["title"],
                content=result["content"],
                author=result.get("author")
            )
        except Exception as e:
            print(f"Create document error: {str(e)}")
            raise Exception(f"Failed to create document: {e}") from e

schema = strawberry.Schema(query=Query, mutation=Mutation)