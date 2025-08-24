import uuid
from fastapi import APIRouter, HTTPException, Request, Path
from fastapi.responses import JSONResponse
from app.db.db import update_match, create_match, delete_match
import datetime
router = APIRouter()

# Static users with fixed session_ids
USERS = [
    {"username": "admin1", "password": "admin@1", "session_id": str(uuid.uuid4())},
    {"username": "admin2", "password": "admin@2", "session_id": str(uuid.uuid4())},
    {"username": "admin3", "password": "admin@3", "session_id": str(uuid.uuid4())},
    {"username": "admin4", "password": "admin@4", "session_id": str(uuid.uuid4())},
    {"username": "admin5", "password": "admin@5", "session_id": str(uuid.uuid4())},
    {"username": "admin6", "password": "admin@6", "session_id": str(uuid.uuid4())},
]

@router.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    for user in USERS:
        if user["username"] == username and user["password"] == password:
            response = JSONResponse(
                status_code=200,
                content={"message": "Login successful", "session_id": user["session_id"]}
            )
            return response

    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/matches/{method}")
async def leaderboard(
    request: Request,
    method: str = Path(...)
):
    data = await request.json()
    print(data)
    print(USERS)
    session_id = data.get("session_id", None)
    print(session_id)
    if session_id is None:
        raise HTTPException(status_code=401, detail="Missing session_id in payload")

    is_admin = False
    for user in USERS:
        if user["session_id"] == session_id:
            is_admin = True
            break
    if not is_admin:
        raise HTTPException(status_code=403, detail="Wrong session_id")
    if method == "update":
        if await update_match(data):
            return JSONResponse(
                status_code=200,
                content={"message": "Data updated successfully"}
            )
    elif method == "create":
        if await create_match(data):
            return JSONResponse(
                status_code=200,
                content={"message": "Data created successfully"}
            )
    elif method == "delete":
        if await delete_match(data):
            return JSONResponse(
                status_code=200,
                content={"message": "Data deleted successfully"}
            )
    raise HTTPException(status_code=400, detail="Invalid data")