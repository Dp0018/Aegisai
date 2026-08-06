from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.documents import router as documents_router
from app.api.v1.rag import router as rag_router

api_router = APIRouter()

# Register v1 routes
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(documents_router, prefix="/documents", tags=["Knowledge Documents"])
api_router.include_router(rag_router, prefix="/rag", tags=["RAG Retrieval"])
