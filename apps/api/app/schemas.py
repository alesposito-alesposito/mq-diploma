from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ThreadOut(BaseModel):
    id: int
    account_id: int
    subject: Optional[str]
    last_message_at: Optional[datetime]
    unread_count: int
    folder: Optional[str]
    class Config:
        from_attributes = True

class MessageOut(BaseModel):
    id: int
    thread_id: Optional[int]
    subject: Optional[str]
    from_addr: Optional[str]
    to_addrs: Optional[str]
    date: Optional[datetime]
    body_html: Optional[str]
    body_text: Optional[str]
    has_attachments: bool
    class Config:
        from_attributes = True

class NoteIn(BaseModel):
    blocks_json: Dict[str, Any]

class NoteOut(BaseModel):
    id: int
    thread_id: int
    author_user_id: Optional[int]
    blocks_json: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class PaginatedThreads(BaseModel):
    items: List[ThreadOut]
    total: int
    page: int
    page_size: int
