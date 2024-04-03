from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Annotated
from database import get_user, register_user
from models import TokenData, Token, User, UserLogin
from jose import JWTError, jwt

app = FastAPI(prefix="/api", title="User Registration and Authentication API")


# Initialize Passlib's CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "1c6b3c0e9fbd0fb47fe187b1ee7f8f62ed481366d34f5ca3e667d39accd4b51f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize an OAuth2PasswordBearer object with the location of the token endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to verify a plaintext password against a hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to authenticate a user using a email and password
# Function to authenticate a user using an email and password
async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user or not verify_password(password, user["password"]):
        return None
    return user


# Function to create a new access token with the provided data and expiration time
def create_access_token(data: dict, expires_delta: Annotated[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency function to retrieve the current user from the provided access token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception

        token_data = TokenData(email=email)
    except JWTError:
        raise credential_exception

    user = get_user(email=token_data.email)
    if user is None:
        raise credential_exception

    return user


# Route for user registration
@app.post("/register/")
async def register_user_route(user: User):
    try:
        # Check if email already exists
        existing_user = await get_user(
            user.email
        )  # If this doesn't throw an error then the email is already registered
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

        hashed_password = pwd_context.hash(user.password)
        user_data = {
            "username": user.username,
            "email": user.email,
            "password": hashed_password,
        }
        await register_user(user_data)
        return {"message": "User registered successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Route for user login
@app.post("/login/", response_model=Token)
async def login_user_route(form_data: UserLogin):
    print(form_data.email)
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
