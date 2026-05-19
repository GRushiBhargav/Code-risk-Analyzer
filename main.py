from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.app.routes import webhook
from backend.app.database.session import engine, Base
from backend.app.models import models  # ← correct path


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(webhook.router)
