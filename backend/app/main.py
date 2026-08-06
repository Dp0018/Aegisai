from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title="AegisAI Backend Platform",
    description="Minimal entrypoint for AegisAI local service validation",
    version="0.1.0"
)

# Set up CORS middleware to allow cross-origin requests from the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows local dev servers on any port (e.g. 3000, 3001)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
