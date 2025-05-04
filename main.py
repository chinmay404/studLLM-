from fastapi import FastAPI
from mangum import Mangum
import json
from app.routers import ai_response
from contextlib import asynccontextmanager
from Agents.main import getGraphResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


@asynccontextmanager
async def _init_graph(app: FastAPI):
    print("Initializing Graph")
    graph = getGraphResponse()
    if not graph:
        raise RuntimeError("Failed To Init LLM Graph")
    else:
        print("Finished checking LLM.")
    yield

app = FastAPI(
    title="studLLm API",
    description="A studLLm API",
    version="1.0.0",
    # lifespan=_inizzdt_graph
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_response.router, prefix="/api/v1", tags=["Chat"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
