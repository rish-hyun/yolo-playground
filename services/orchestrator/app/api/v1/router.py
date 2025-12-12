from fastapi import APIRouter

from .tasks import router as tasks_router
from .vision import router as vision_router

api_router = APIRouter()

api_router.include_router(tasks_router, prefix="/tasks")
api_router.include_router(vision_router, prefix="/vision")
