from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from ..services.email_sender import send_email

router = APIRouter(prefix="/compose", tags=["compose"])

class ComposeIn(BaseModel):
    account_id: int
    to: List[EmailStr]
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
    subject: str
    body_text: Optional[str] = None
    body_html: Optional[str] = None

@router.post("")
async def compose(payload: ComposeIn):
    await send_email(
        account_id=payload.account_id,
        to=payload.to,
        cc=payload.cc or [],
        bcc=payload.bcc or [],
        subject=payload.subject,
        body_text=payload.body_text or "",
        body_html=payload.body_html,
    )
    return {"status": "queued"}
