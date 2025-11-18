from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from app.admin.views import AdminPermission, AdminRole, AdminUser
from app.database import engine
from app.users.router import router as router_user


app = FastAPI()
app.include_router(router_user)
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
