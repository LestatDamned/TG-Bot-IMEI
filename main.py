import logging

import uvicorn
from fastapi import FastAPI, HTTPException

from config import API_TOKEN
from utils import imei_validator, check_imei

app = FastAPI()


@app.post("/api/check-imei")
async def api_check_imei(imei: str, token: str) -> dict:
    """Ендпоинт для проверки IMEI"""

    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Неверный токен")

    try:
        imei_validator(imei)
    except ValueError as e:
        return {f"error": f"{e}"}

    result = await check_imei(imei)
    return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    uvicorn.run("main:app", host="127.0.0.1", port=8000)