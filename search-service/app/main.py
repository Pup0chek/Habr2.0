from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn

from .services.elastic import perform_search

SEARCH_REQUESTS = Counter('search_requests_total', 'Total number of search requests')

app = FastAPI(title="Search Service",
              description="Микросервис поиска с использованием Elasticsearch и Prometheus",
              )




Instrumentator().instrument(app).expose(app)
# Добавляем CORS, если фронтенду нужно обращаться к сервису
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Search Service is running"}

@app.get("/search")
async def search(q: str):
    SEARCH_REQUESTS.inc()
    results = perform_search(q)
    return {"query": q, "results": results}

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
