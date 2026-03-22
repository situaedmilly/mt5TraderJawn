from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health, heartbeats, journal, proposals, signals


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="mt5TraderJawn", lifespan=lifespan)
app.include_router(health.router)
app.include_router(heartbeats.router)
app.include_router(signals.router)
app.include_router(journal.router)
app.include_router(proposals.router)
