from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqladmin import Admin
from app.database import engine
from app.admin.views import AdminUser, AdminRole, AdminPermission
from app.users.router import router as router_user
from app.pages.router import router as router_pages
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router_user)
app.include_router(router_pages)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


admin_panel = Admin(app, engine, title="Admin Panel")

admin_panel.add_view(AdminUser)
admin_panel.add_view(AdminRole)
admin_panel.add_view(AdminPermission)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Accept", "Accept-Language", "Content-Language", "Content-Type", "Authorization", "Cookie", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "X-Requested-With", "Origin", "User-Agent", "Referer","Host"],
)



@app.get("/")
async def root():
    return {"message": "API is running"}

@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/front/t_login", status_code=status.HTTP_303_SEE_OTHER)
