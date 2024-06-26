from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import Depends, FastAPI
import fastapi_users
from pydantic import BaseModel, Field

from src.auth.manager import get_user_manager
from src.database import User
from src.auth.schemas import UserCreate, UserRead
from src.auth.config import auth_backend
from fastapi_users import FastAPIUsers


app = FastAPI(
    title="Test App"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def protected_route():
    return f"Hello, anonym"

@app.post("/plus/{num1}/{num2}")
def adding_numbers(num1: int, num2: int):
    return f"Ответ = {num1 + num2}"
