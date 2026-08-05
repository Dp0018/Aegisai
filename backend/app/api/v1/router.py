from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.documents import router as documents_router

api_router = APIRouter()

# Register v1 routes
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(documents_router, prefix="/documents", tags=["Knowledge Documents"])
