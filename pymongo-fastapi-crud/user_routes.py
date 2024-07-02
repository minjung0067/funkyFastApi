from fastapi import APIRouter, HTTPException, Request, Depends
from models import User, UserLogin, UserCreate
from hashing import verify_password, get_password_hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

router = APIRouter()

@router.post("/signup", response_model=User)
async def create_user(user: UserCreate, request: Request):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))

    try:
        # 이메일 중복 확인
        if request.app.database["users"].find_one({"email": user_dict["email"]}):
            raise HTTPException(status_code=400, detail="Email already registered")

        # 사용자 생성
        new_user = request.app.database["users"].insert_one(user_dict)

        if new_user.inserted_id:
            created_user = request.app.database["users"].find_one({"_id": new_user.inserted_id})
            created_user["id"] = str(created_user["_id"])
            return User(**created_user)
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/login", response_model=User)
async def login_user(user: UserLogin, request: Request):
    user_dict = request.app.database["users"].find_one({"email": user.email})

    if not user_dict:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(user.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user_dict["id"] = str(user_dict["_id"])
    return User(**user_dict)