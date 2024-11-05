from pydantic import BaseModel, HttpUrl
from typing import Dict, Any

class WebhookRequest(BaseModel):
    message: str
    callback_url: HttpUrl

class WebhookResponse(BaseModel):
    status: str

class CallbackRequest(BaseModel):
    data: Dict[str, Any]

class CallbackResponse(BaseModel):
    status: str
    data: Dict[str, Any]