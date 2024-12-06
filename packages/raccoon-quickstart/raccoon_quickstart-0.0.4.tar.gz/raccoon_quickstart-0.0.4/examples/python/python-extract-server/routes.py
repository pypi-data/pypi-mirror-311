import os

import requests
from dotenv import load_dotenv
from fastapi import Request, APIRouter
from starlette.responses import StreamingResponse, JSONResponse
from typing import AsyncGenerator

router = APIRouter()

@router.post("/lam/extract")
async def call_raccoon_api(request: Request, app_name: str):
    try:
        load_dotenv()
        raccoon_passcode = request.headers.get("raccoon-passcode", "")
        secret_key = os.environ.get("RACCOON_SECRET_KEY")

        request_body = await request.json()
        if not raccoon_passcode:
            return JSONResponse(content={"error": "Missing 'raccoon-passcode' header."}, status_code=400)

        response = requests.post(
            f"https://api.flyingraccoon.tech/lam/extract",
            json=request_body,
            headers={
                "Content-Type": "application/json",
                "raccoon-passcode": raccoon_passcode,
                "secret-key": secret_key,
            }
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)

    except Exception:
        return JSONResponse(content="Internal Server Error", status_code=500)
