from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import health, threads, messages, notes, compose, actions, sync

app = FastAPI(title="Mail API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(',')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(threads.router)
app.include_router(messages.router)
app.include_router(notes.router)
app.include_router(compose.router)
app.include_router(actions.router)
app.include_router(sync.router)
