from typing import Annotated
from fastapi import FastAPI, Body, HTTPException
from passlib.context import CryptContext
from database import register_user, user_collection
from models import UserLogin, UserRegistration


app = FastAPI(prefix="/api", title="User Registration and Authentication API")


# Initialize Passlib's CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# OAuth2 token URL configuration




@app.post("/register", response_model=UserRegistration)
async def register_user_route(user: Annotated[UserRegistration, Body(embed=True)]):
    # Check if email already exists
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Perform user registration
    response = await register_user(user)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


@app.post("/login")
async def login_user(user: UserLogin = Body(...)):
    stored_user = user_collection.find_one({"username": user.username})
    if not stored_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not pwd_context.verify(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", "user": stored_user}