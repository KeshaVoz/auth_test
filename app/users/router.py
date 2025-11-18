from fastapi import APIRouter, HTTPException, Response, Form
from app.users.dao import UserDAO
from app.users.schemas import SUserRegister, SUserLogin
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from typing import Annotated

router = APIRouter(
    tags=["Auth & Users & Meow"]
)

@router.post("/register")
async def register_user(user_data:  Annotated[SUserRegister, Form()]):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException()
    hashed_password = get_password_hash(user_data.password)
    user_data = user_data.model_dump(exclude={"password"})
    user_data['hashed_password'] = hashed_password
    await UserDAO.add_user_with_role(user_data)
    user = await UserDAO.find_one_or_none(email=user_data['email'])
    access_token = create_access_token({"sub": str(user.id)})
    return access_token

@router.post("/login")
async def login_user(user_data:  Annotated[SUserLogin, Form()]): 
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException()
    access_token = create_access_token({"sub": str(user.id)})
    return access_token

@router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie("auth_test_access_token")