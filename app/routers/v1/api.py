from fastapi import APIRouter
from app.routers.v1 import (
    health,
    registrationLogin,
    expense,
    dashboard,
    ai
)


api_routes = APIRouter()

api_routes.include_router(health.router)
api_routes.include_router(registrationLogin.router)
api_routes.include_router(expense.router)
api_routes.include_router(dashboard.router)
api_routes.include_router(ai.router)