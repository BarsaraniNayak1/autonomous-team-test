from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import datetime
from typing import Dict

app = FastAPI(title="Social Network API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database for users
users_db: Dict[str, dict] = {}

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    email: str
    created_at: str
    token: str

@app.post("/api/auth/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegisterSchema):
    if user_data.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )
    
    user_id = len(users_db) + 1
    created_at = datetime.datetime.utcnow().isoformat()
    user_record = {
        "id": user_id,
        "email": user_data.email,
        "password": user_data.password,
        "created_at": created_at
    }
    users_db[user_data.email] = user_record
    
    return {
        "id": user_id,
        "email": user_data.email,
        "created_at": created_at,
        "token": f"mock-jwt-token-for-{user_id}"
    }
