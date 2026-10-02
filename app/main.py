import os
from fastapi import FastAPI
from app.routers.v1.api import api_routes
from contextlib import asynccontextmanager
from app.database.init_db import create_tables
from app.core.exceptions import global_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URLS = [
    url.strip()
    for url in os.getenv("FRONTEND_URLS", "").split(",")
    if url.strip()
]


@asynccontextmanager
async def lifespan(app: FastAPI):

    create_tables()

    yield

app = FastAPI(
    title="Expense Tracking App",
    description="Backend API for an AI-powered Expense Tracker",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        *FRONTEND_URLS,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)

app.include_router(api_routes,prefix="/api/v1")

@app.get("/")
def home():
    return {
        "msg":"Welcome to expense tracking app."
    }
