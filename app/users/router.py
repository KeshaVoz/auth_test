from fastapi import APIRouter, HTTPException, Request, Response, Depends, Form
from app.users.dao import UserDAO
from app.users.schemas import SUserRegister, SUser, SUserLogin
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.models import User
from app.users.dependencies import get_current_user
from typing import Annotated
from fastapi.responses import RedirectResponse
from fastapi import status, Query
from app.users.dependencies import change_user_schema

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
    redirect_response = RedirectResponse(url="/front/my_info", status_code=status.HTTP_303_SEE_OTHER)
    redirect_response.set_cookie("auth_test_access_token", access_token, httponly=True)
    return redirect_response

@router.post("/login")
async def login_user(response: Response, user_data:  Annotated[SUserLogin, Form()]): 
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException()
    if user.is_active == False:
        raise HTTPException()
    access_token = create_access_token({"sub": str(user.id)})
    redirect_response = RedirectResponse(url="/front/my_info", status_code=status.HTTP_303_SEE_OTHER)
    redirect_response.set_cookie("auth_test_access_token", access_token, httponly=True)
    return redirect_response

@router.get("/logout")
async def logout_user(response: Response, delete: bool = Query(default=False), current_user: User = Depends(get_current_user)):
    if delete:
        await UserDAO.soft_delete_user(current_user.id)
    response.delete_cookie("auth_test_access_token")
    return RedirectResponse(url="/front/t_login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/my_info/lucky_number")
async def get_lucky_number(current_user: User = Depends(get_current_user)):
    lucky_number = current_user.user_data
    return {"lucky_number": lucky_number}

@router.patch("/my_info/change")
async def change_info(request: Request, current_user: User = Depends(get_current_user)):
    data = await request.json()
    await UserDAO.update_data(current_user.id, **data)
    