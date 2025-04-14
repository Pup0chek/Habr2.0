from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .schema import schema
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()


Instrumentator().instrument(app).expose(app)
# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Разрешаем запросы от любых источников (на продакшене ограничьте список доменов)
    allow_credentials=True,
    allow_methods=["*"],          # Разрешаем все методы, включая OPTIONS
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema, graphiql=True)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

