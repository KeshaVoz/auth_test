from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
