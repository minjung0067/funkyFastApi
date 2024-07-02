import uuid
from typing import Optional
from pydantic import BaseModel, Field, EmailStr #Email용

class Book(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    synopsis: str = Field(...)
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "1",
                "title": "가나다",
                "author": "작가",
                "synopsis": "..."
            }
        }


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    synopsis: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "Don Quixote is a Spanish novel by Miguel de Cervantes..."
            }
        }


#User
class User(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: EmailStr
    hashed_password: str
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "username": "funky",
                "email": "minjung@example.com",
                "hashed_password": "hashedpassword"
            }
        }

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "username": "funky",
                "email": "minjung@example.com",
                "password": "password"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "minjung@example.com",
                "password": "password"
            }
        }