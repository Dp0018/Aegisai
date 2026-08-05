from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title="AegisAI Backend Platform",
    description="Minimal entrypoint for AegisAI local service validation",
    version="0.1.0"
)

# Register central routers
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/health", tags=["Health"])
async def health_check():
    """Verify backend server connectivity."""
    return {
        "status": "healthy",
        "service": "AegisAI Backend"
    }
