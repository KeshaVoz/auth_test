from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.users.models import User
from app.users.dependencies import get_current_user
from app.users.schemas import SUser

router = APIRouter(
    prefix="/front",
    tags=["Frontend"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/t_reg")
async def register_page(request: Request):
    return templates.TemplateResponse(name="register.html", context={"request": request})

@router.get("/t_login")
async def login_page(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})

@router.get("/my_info")
async def main_page(request: Request, current_user: User = Depends(get_current_user)):
    user = SUser.model_validate(current_user)
    return templates.TemplateResponse(name="my_info.html", context={"request": request, "user": user})

@router.get("/my_info/change")
async def main_page(request: Request, current_user: User = Depends(get_current_user)):
    user = SUser.model_validate(current_user)
    return templates.TemplateResponse(name="change_info.html", context={"request": request, "user": user})