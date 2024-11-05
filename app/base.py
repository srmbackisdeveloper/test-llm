import logging
import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from app.db.connection import init_db
from app.models import WebhookRequest, WebhookResponse, CallbackRequest, CallbackResponse
from llm.assistant import get_assistant_response

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    init_db()
    logger.info("Database initialized")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")


@app.post("/webhook", response_model=WebhookResponse)
async def handle_webhook(request: WebhookRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_and_send_response, request)
    return WebhookResponse(status="processing")

async def process_and_send_response(request: WebhookRequest):
    try:
        test_user_id = "011"  # для теста, обычно гарантируется, что id - unique
        response_text = await get_assistant_response(user_id=test_user_id, content=request.message)

        callback_url = str(request.callback_url)
        await send_callback(callback_url, {"data": {"message": response_text}})

    except Exception as e:
        logger.error(f"Error processing webhook request: {e}")

async def send_callback(callback_url: str, data: dict):
    async with httpx.AsyncClient() as client:
        try:
            await client.post(callback_url, json=data)
            logger.info(f"Callback sent to {callback_url} successfully.")
        except Exception as e:
            logger.error(f"Error sending callback to {callback_url}: {e}")


@app.post("/callback", response_model=CallbackResponse)
async def callback_test(request: CallbackRequest):
    logger.info("Received callback data: %s", request.data)
    return CallbackResponse(status="received", data=request.data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)