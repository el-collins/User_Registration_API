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


async def register_user(user_data):
    try:
        hashed_password = pwd_context.encrypt(user_data['password'])
        user_data['password'] = hashed_password
        result = await user_collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id  # Add the database-generated ID to user data
        return user_data
    except Exception as e:
        raise ValueError("Failed to register user") from e


async def login_user(email: str, password: str):
    # Find the user by email in the database
    stored_user = await user_collection.find_one({"email": email})
    if not stored_user:
        # If user with the provided email does not exist
        raise ValueError("User with this email does not exist")
    
    # Verify the password
    if not pwd_context.verify(password, stored_user["password"]):
        # If the password does not match
        raise ValueError("Invalid password")

    # If everything is correct, return the user data without the password
    return stored_user
    # return {key: value for key, value in stored_user.items() if key != "password"}