import httpx
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

async def get_open_ended_schemes(fund_family: str, token: str):
    url = f"https://latest-mutual-fund-nav.p.rapidapi.com/latest"
    
    # Set the static Scheme_Type parameter
    params = {
        "Mutual_Fund_Family": fund_family,
        "Scheme_Type": "Open"
    }
    
    headers = {
        "x-rapidapi-host": "latest-mutual-fund-nav.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data")
    
    return response.json()
