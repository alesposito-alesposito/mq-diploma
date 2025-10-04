from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Message
from ..schemas import MessageOut

router = APIRouter(prefix="/messages", tags=["messages"])

@router.get("/{message_id}", response_model=MessageOut)
def get_message(message_id: int, db: Session = Depends(get_db)):
    obj = db.get(Message, message_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Message not found")
    return obj
