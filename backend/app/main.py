from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text
import logging

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import engine
from app.core.kafka import (
    init_kafka_producer,
    close_kafka_producer,
    start_kafka_consumers,
    stop_kafka_consumers
)

logger = logging.getLogger("aegisai.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure schema updates (e.g. user_id column) exist in deployed DB
    try:
        async with engine.begin() as conn:
            await conn.execute(text("ALTER TABLE documents ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id) ON DELETE CASCADE;"))
            await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_documents_user_id ON documents (user_id);"))
    except Exception as e:
        logger.warning(f"Database auto-migration notice: {e}")

    await init_kafka_producer()
    await start_kafka_consumers()
    yield
    # Shutdown
    await stop_kafka_consumers()
    await close_kafka_producer()

app = FastAPI(
    title="AegisAI Backend Platform",
    description="Minimal entrypoint for AegisAI local service validation",
    version="0.1.0",
    lifespan=lifespan
)

# Global unhandled exception handler to always preserve CORS headers on 500s
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception on {request.method} {request.url.path}: {exc}")
    origin = request.headers.get("origin") or "*"
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"},
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Expose Prometheus metric endpoint
Instrumentator().instrument(app).expose(app)

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
