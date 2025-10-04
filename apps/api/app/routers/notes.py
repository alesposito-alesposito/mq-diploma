from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Note
from ..schemas import NoteIn, NoteOut

router = APIRouter(prefix="/threads", tags=["notes"])

@router.get("/{thread_id}/notes", response_model=list[NoteOut])
def list_notes(thread_id: int, db: Session = Depends(get_db)):
    rows = db.query(Note).filter(Note.thread_id == thread_id).order_by(Note.created_at.asc()).all()
    return rows

@router.post("/{thread_id}/notes", response_model=NoteOut)
def create_note(thread_id: int, payload: NoteIn, db: Session = Depends(get_db)):
    note = Note(thread_id=thread_id, blocks_json=payload.blocks_json)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
