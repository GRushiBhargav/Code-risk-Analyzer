from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.app.routes import webhook
from backend.app.routes import frontend_analytics
from backend.app.database.session import engine, Base
from backend.app.models import models  # ← correct path
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(webhook.router)
app.include_router(frontend_analytics.router)
