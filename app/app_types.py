from pydantic import BaseModel, HttpUrl
from typing import Dict, Any, List
from datetime import datetime

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

class Message(BaseModel):
    role: str
    time: datetime
    message: str

class UserMessagesRequest(BaseModel):
    user_id: str

class UserMessagesResponse(BaseModel):
    user_id: str
    messages: List[Message]
