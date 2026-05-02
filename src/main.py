import logging
import uuid

from fastapi import FastAPI, Request
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("webhook-relay")

app = FastAPI(title="ZI Webhook Relay")


class ForwardRequest(BaseModel):
    url: str
    payload: dict


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    webhook_id = str(uuid.uuid4())
    logger.info("Received webhook %s: %s", webhook_id, body)
    return {"received": True, "id": webhook_id}


@app.post("/webhook/forward")
async def forward_webhook(forward_request: ForwardRequest):
    logger.info(
        "Forwarding webhook to %s with payload: %s",
        forward_request.url,
        forward_request.payload,
    )
    return {"forwarded": True, "target": forward_request.url}
