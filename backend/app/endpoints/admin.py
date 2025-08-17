import uuid
from fastapi import APIRouter, HTTPException, Request, Cookie, Path
from fastapi.responses import JSONResponse
from app.db.db import update_match, create_match
import datetime
router = APIRouter()

# Static users with fixed session_ids
USERS = [
    {"username": "a", "password": "a", "session_id": str(uuid.uuid4())},
    {"username": "admin", "password": "pass123", "session_id": str(uuid.uuid4())},
    {"username": "mod1", "password": "mod123", "session_id": str(uuid.uuid4())},
    {"username": "player1", "password": "p123", "session_id": str(uuid.uuid4())},
    {"username": "user1", "password": "u123", "session_id": str(uuid.uuid4())},
    {"username": "guest", "password": "g123", "session_id": str(uuid.uuid4())},
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

def serialize_doc(doc):
    for k, v in doc.items():
        if isinstance(v, datetime.datetime):
            doc[k] = v.isoformat()
    return doc

@router.post("/matches/{method}")
async def leaderboard(
    request: Request,
    method: str = Path(...)
):
    # session_id = request.cookies.get("session_id")
    # if session_id is None or session_id not in [user["session_id"] for user in USERS]:
    #     raise HTTPException(status_code=401, detail="Missing session_id cookie")

    # for user in USERS:
    #     if user["session_id"] == session_id:
    data = await request.json()
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
    raise HTTPException(status_code=400, detail="Invalid data")
