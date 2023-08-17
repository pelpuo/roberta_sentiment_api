import fastapi
import uvicorn
from fastapi import responses
from fastapi.middleware.cors import CORSMiddleware

from routers import classify
from core.config import roberta
import os

from dotenv import load_dotenv
load_dotenv()

ORIGIN = os.getenv("ORIGIN")

app = fastapi.FastAPI()

origins = [ORIGIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
