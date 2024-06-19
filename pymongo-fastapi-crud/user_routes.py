from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from pymongo.database import Database
from models import User, UserCreate
from hashing import get_password_hash

router = APIRouter()

@router.post("/signup", response_model=User)
async def create_user(user: UserCreate, request: Request):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))

    # 이메일 중복 확인
    if request.app.database["users"].find_one({"email": user_dict["email"]}):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = request.app.database["users"].insert_one(user_dict)
    created_user = request.app.database["users"].find_one({"_id": new_user.inserted_id})
    return User(**created_user)
