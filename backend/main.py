"""FastAPI application entrypoint for the backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import events, homepage, homework, tasks, time_entries

app = FastAPI()

# Includes all routers
app.include_router(tasks.router)
app.include_router(events.router)
app.include_router(homework.router)
app.include_router(time_entries.router)
app.include_router(homepage.router)

# Enabled CORS for front-end access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # replace with front-end URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
