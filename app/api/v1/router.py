from fastapi import APIRouter

from .task_types.routes import router as task_types_router

api_router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)
api_router.include_router(task_types_router)
