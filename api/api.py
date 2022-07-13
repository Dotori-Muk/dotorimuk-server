from fastapi import APIRouter
from . import apply


router = APIRouter()


router.include_router(apply.router, tags=["apply"], prefix="/apply")
