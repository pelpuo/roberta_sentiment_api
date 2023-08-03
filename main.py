import fastapi
import uvicorn
from fastapi import responses

from routers import classify
from core.config import roberta
import os

app = fastapi.FastAPI()

@app.on_event("startup")
def startup_event():
    roberta.initialize()

app.include_router(classify.router, tags=["translate"])


@app.get("/", include_in_schema=False)
async def index() -> responses.RedirectResponse:
    return responses.RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8185,
        reload=True,
    )
