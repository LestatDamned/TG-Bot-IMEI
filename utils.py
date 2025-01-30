import httpx

from config import API_TOKEN

def imei_validator(imei: str) -> str:
    """Валидатор IMEI"""

    if not imei.isdigit():
        raise ValueError("IMEI должен состоять из цифр")

    if len(imei) != 15:
        raise ValueError("IMEI должен быть длинной 15 символов")

    return imei


async def check_imei(imei: str) -> dict:
    """Функция проверки IMEI"""

    url = "https://api.imeicheck.net/v1/checks"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "deviceId": imei,
        "serviceId": 12
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"Ошибка HTTP: {e.response.status_code}",
                    f"details": f"{response.json()}"}
