# gateway/app/resolvers/user_resolver.py
import strawberry

@strawberry.type
class User:
    id: int
    username: str

def get_user(user_id: int) -> User:
    # Здесь можно вызвать внешний сервис или базу данных
    return User(id=user_id, username="demo_user")
