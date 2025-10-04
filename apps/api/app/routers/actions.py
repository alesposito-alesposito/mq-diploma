from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Literal

router = APIRouter(prefix="/actions", tags=["actions"])

class ActionIn(BaseModel):
    message_id: int
    action: Literal["star", "unstar", "read", "unread", "snooze"]

@router.post("")
async def perform_action(payload: ActionIn):
    # Stub: In a real implementation, update flags in DB and enqueue sync
    return {"ok": True}
