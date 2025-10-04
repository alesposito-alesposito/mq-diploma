from fastapi import APIRouter

router = APIRouter(prefix="/sync", tags=["sync"])

@router.post("/{account_id}/start")
async def start_sync(account_id: int):
    # Stub: enqueue celery task to sync IMAP
    return {"status": "started", "account_id": account_id}
