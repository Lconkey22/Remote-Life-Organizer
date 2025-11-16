from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

fake_users = [
    {"id": 1, "name": "Chelsie"},
    {"id": 2, "name": "Lindsey"},
    {"id": 3, "name": "Nathan"}
]

@router.get("/")
def get_users():
    return fake_users
