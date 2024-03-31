from fastapi import FastAPI, Body
from pydantic import BaseModel, EmailStr, StringConstraints, validator
from typing_extensions import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # noqa: F401



app = FastAPI(title="User Registration API")


# Initialize Passlib's CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# OAuth2 token URL configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




# Mock database for demonstration purposes
fake_users_db = {
    "johndoe@example.com": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": pwd_context.hash("secret")
    }
}


class UserRegistration(BaseModel):
    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=3,
            max_length=50,
            pattern=r"^[a-zA-Z0-9_-]+$",
            
        ),
    ]
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8, max_length=50)]

    @validator("password")
    def validate_password(cls, value):
        # Check for password complexity requirements
        if (
            len(value) < 8
            or not any(char.isdigit() for char in value)
            or not any(char.isupper() for char in value)
            or not any(char.islower() for char in value)
        ):
            raise ValueError(
                "Password must be at least 8 characters long, include a number, an uppercase letter, and a lowercase letter"
            )
         # Hash the password using passlib
        return pwd_context.hash(value)


@app.post("/register")
async def register_user(user: Annotated[UserRegistration, Body(embed=True)]):
    
    hashed_password = pwd_context.hash(user.password)
    print(f"User registered: {user.username} - {hashed_password}")
    # Ensure that the provided username and email are unique
    # Simulated user registration process
    # Here you would typically save the user to a database or perform other actions
    return {"message": "User registered successfully", "user": user.dict()}


# Simulate registration process with FastAPI TestClient
# client = TestClient(app)


# def test_register_valid_user():
#     user_data = {
#         "username": "user123",
#         "email": "user123@example.com",
#         "password": "StrongPassword123",
#     }
#     response = client.post("/register", json=user_data)
#     assert response.status_code == 200
#     assert response.json() == {
#         "message": "User registered successfully",
#         "user": user_data,
#     }


# def test_register_invalid_user():
#     user_data = {
#         "username": "user",  # Invalid username (less than 3 characters)
#         "email": "invalidemail",  # Invalid email format
#         "password": "weak",  # Password does not meet complexity requirements
#     }
#     response = client.post("/register", json=user_data)
#     assert response.status_code == 422  # Expecting validation error
