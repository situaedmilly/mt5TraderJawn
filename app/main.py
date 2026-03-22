from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, heartbeats, signals, journal, proposals
from app.core.config import get_settings
from app.core.logging import setup_logging
settings = get_settings()
setup_logging()
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    yield
    # Shutdown
app = FastAPI(
    title="Trading Stack API",
    description="Systematic trading control stack",
    version="0.1.0",
    lifespan=lifespan,
)
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register routes
app.include_router(health.router, tags=["health"])
app.include_router(heartbeats.router, prefix="/heartbeats", tags=["heartbeats"])
app.include_router(signals.router, prefix="/signals", tags=["signals"])
app.include_router(journal.router, prefix="/journal", tags=["journal"])
app.include_router(proposals.router, prefix="/proposals", tags=["proposals"])
