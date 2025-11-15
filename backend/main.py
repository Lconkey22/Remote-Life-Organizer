from fastapi import FastAPI
from routers import tasks, events, users

app = FastAPI(
    title="Remote Life Organizer API",
    description="Backend for the Remote Life Organizer student productivity app.",
    version="1.0"
)

app.include_router(tasks.router)
app.include_router(events.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Remote Life Organizer API is running!"}
