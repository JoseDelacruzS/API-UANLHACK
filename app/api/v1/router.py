from fastapi import APIRouter
from app.api.v1.endpoints import (
    operators,
    clients,
    calls,
    tickets,
    dashboards,
    reports,
    watson
)

api_router = APIRouter()

# Incluir todos los routers de endpoints
api_router.include_router(
    operators.router,
    prefix="/operators",
    tags=["operators"]
)

api_router.include_router(
    clients.router,
    prefix="/clients",
    tags=["clients"]
)

api_router.include_router(
    calls.router,
    prefix="/calls",
    tags=["calls"]
)

api_router.include_router(
    tickets.router,
    prefix="/tickets",
    tags=["tickets"]
)

api_router.include_router(
    dashboards.router,
    prefix="/dashboards",
    tags=["dashboards"]
)

api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["reports"]
)

api_router.include_router(
    watson.router,
    prefix="/watson",
    tags=["watson-orchestrate"]
)
