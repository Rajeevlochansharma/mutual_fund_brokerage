from fastapi import HTTPException, Security, Depends, Header
from dotenv import load_dotenv
import os

load_dotenv()

DUMMY_USERNAME = os.getenv("DUMMY_USERNAME")
DUMMY_PASSWORD = os.getenv("DUMMY_PASSWORD")

async def authenticate(username: str, password: str):
    if username == DUMMY_USERNAME and password == DUMMY_PASSWORD:
        return {"access_token": "fake-token", "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")

async def fake_decode_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
    
    token = authorization.split(" ")[1]  # Extract the token

    # Here, you should check if the token matches the expected value
    expected_token = "your_expected_token"  # Replace this with your expected token
    if token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token

