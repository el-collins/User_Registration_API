from fastapi import Body, FastAPI, HTTPException
from passlib.context import CryptContext
from typing import Annotated
from database import login_user, register_user, user_collection
from models import UserLogin, UserRegistration

app = FastAPI(prefix="/api", title="User Registration and Authentication API")


# Initialize Passlib's CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# OAuth2 token URL configuration


@app.post("/register", response_model=UserRegistration)
async def register_user_route(user: Annotated[UserRegistration, Body(embed=True)]):

    try:
        # Check if email already exists
        existing_user = await user_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Perform user registration
        response = await register_user(user.dict())
        if response:
            return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login", response_model=UserLogin)
async def login_user_route(user: Annotated[UserLogin, Body(embed=True)]):
    
    try:
        response = await login_user(user.email, user.password)
        if response:
            print("Successfully logged in")
            return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
