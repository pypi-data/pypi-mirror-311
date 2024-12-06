import os
from typing import AsyncGenerator

import requests
from dotenv import load_dotenv
from fastapi import Request, APIRouter
from starlette.responses import StreamingResponse, JSONResponse

router = APIRouter()


@router.post("/lam/run")
async def call_raccoon_api(request: Request):
    try:
        load_dotenv()
        raccoon_passcode = request.headers.get("raccoon-passcode", "")
        secret_key = os.environ.get("RACCOON_SECRET_KEY")

        request_body = await request.json()
        if not raccoon_passcode:
            return JSONResponse(content={"error": "Missing 'raccoon-passcode' header."}, status_code=400)

        stream = request_body.get("stream", False)

        response = requests.post(
            "https://api.flyingraccoon.tech/lam/run",
            json=request_body,
            headers={
                "Content-Type": "application/json",
                "raccoon-passcode": raccoon_passcode,
                "secret-key": secret_key,
            },
            stream=stream
        )

        if stream:
            async def stream_generator() -> AsyncGenerator[bytes, None]:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk

            return StreamingResponse(
                stream_generator(),
                media_type="application/json"
            )
        else:
            return JSONResponse(content=response.json(), status_code=response.status_code)

    except Exception:
        return JSONResponse(content="Internal Server Error", status_code=500)
