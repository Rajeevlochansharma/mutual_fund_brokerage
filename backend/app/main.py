from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.auth import authenticate, fake_decode_token
from app.mutual_funds import get_open_ended_schemes
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel


app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str
    
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/token")
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "admin123":  # Dummy credentials
        return {"access_token": "your_expected_token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/funds/{fund_family}")
async def fetch_funds(fund_family: str, token: str = Depends(fake_decode_token)):
    return await get_open_ended_schemes(fund_family, token)

@app.post("/buy")
async def buy_units(token: str = Depends(fake_decode_token)):
    return {"message": "Purchase successful!"}

