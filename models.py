from pydantic import BaseModel, EmailStr, Field, StringConstraints, validator
from typing_extensions import Annotated

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
    email: EmailStr = Field(..., min_length=6, description="User email")
    password: Annotated[str, StringConstraints(min_length=8)]

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
        return value

class UserLogin(BaseModel):
    username: str
    password: str