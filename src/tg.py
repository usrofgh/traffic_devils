import httpx


async def send_msg_to_tg(bot_token: str, chat_id: str, message: str) -> dict:
    endpoint =  f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, params=params)
    return response.json()
