from fastapi import FastAPI
from app.routers.v1.api import api_routes
from contextlib import asynccontextmanager
from app.database.init_db import create_tables
from app.core.exceptions import global_exception_handler


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
