from fastapi import HTTPException, BackgroundTasks, Request
import httpx
from app.base import app
from app.models import WebhookRequest
from app.settings import OPENAI_API_KEY
from llm.assistant import get_assistant_response

@app.post("/webhook")
async def handle_webhook(request: WebhookRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_and_send_response, request)
    return {"status": "processing"}

async def process_and_send_response(request: WebhookRequest):
    try:
        test_user_id = "11" # для теста, обычно гарантируется, что id - unique
        response_text = await get_assistant_response(user_id=test_user_id, content=request.message)
        await send_callback(request.callback_url, {"message": response_text})

    except Exception as e:
        print(f"Error processing webhook request: {e}")

async def send_callback(callback_url: str, data: dict):
    async with httpx.AsyncClient() as client:
        try:
            await client.post(callback_url, json=data)
        except Exception as e:
            print(f"Error sending callback: {e}")

# ТЕСТ
@app.post("/callback")
async def callback_test(data: dict, request: Request):
    print("Received callback data:", data)
    return {"status": "received", "data": data}