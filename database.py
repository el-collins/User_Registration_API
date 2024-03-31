from models import UserRegistration
from motor.motor_asyncio import (
    AsyncIOMotorClient,
)
from passlib.context import CryptContext


import os
from dotenv import load_dotenv


load_dotenv()


def connectToDB():
    MONGO_URL = os.getenv("MONGO_URL")
    client = AsyncIOMotorClient(MONGO_URL)
    database = client.user_database
    user_collection = database.users
    print("Successfully connected")
    return user_collection


user_collection = connectToDB()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register_user(user: UserRegistration):
    # check if user already exist in the database
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user: 
        raise ValueError("Username already exists")

    # If user does not exist
    hashed_password = pwd_context.hash(user.password)
    user_data = {
            "username": user.username,
            "email": user.email,
            "password": hashed_password
           }
    
    try:
        result = await user_collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id  # Add the database-generated ID to user data
    except Exception as e:
        raise ValueError("Failed to register user") from e

    return user_data  # Return the entire user object
        
async def get_user(email: str):
    return await user_collection.find_one({"email": email})
