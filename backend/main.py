from fastapi import FastAPI
from backend.routers import tasks, events
from backend.routers import homepage  # if you created homepage.py

app = FastAPI()

# Includes all routers
app.include_router(tasks.router)
app.include_router(events.router)
app.include_router(homepage.router)

# Enabled CORS for front-end access
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # replace with front-end URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
