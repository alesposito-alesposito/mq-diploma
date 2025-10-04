from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional
from ..db import get_db
from ..schemas import PaginatedThreads, ThreadOut

router = APIRouter(prefix="/threads", tags=["threads"])

@router.get("", response_model=PaginatedThreads)
def list_threads(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Full-text search query"),
    page: int = 1,
    page_size: int = 20,
):
    offset = (page - 1) * page_size
    if q:
        sql = text(
            """
            SELECT t.* FROM threads t
            JOIN messages m ON m.thread_id = t.id
            WHERE m.indexed_tsvector @@ websearch_to_tsquery('simple', :q)
            GROUP BY t.id
            ORDER BY t.last_message_at DESC NULLS LAST
            LIMIT :limit OFFSET :offset
            """
        )
        total_sql = text(
            """
            SELECT COUNT(DISTINCT t.id) FROM threads t
            JOIN messages m ON m.thread_id = t.id
            WHERE m.indexed_tsvector @@ websearch_to_tsquery('simple', :q)
            """
        )
        rows = db.execute(sql, {"q": q, "limit": page_size, "offset": offset}).mappings().all()
        total = db.execute(total_sql, {"q": q}).scalar_one()
    else:
        sql = text(
            """
            SELECT * FROM threads
            ORDER BY last_message_at DESC NULLS LAST
            LIMIT :limit OFFSET :offset
            """
        )
        total_sql = text("SELECT COUNT(*) FROM threads")
        rows = db.execute(sql, {"limit": page_size, "offset": offset}).mappings().all()
        total = db.execute(total_sql).scalar_one()
    items = [ThreadOut.model_validate(dict(r)) for r in rows]
    return {"items": items, "total": total, "page": page, "page_size": page_size}
