from . import __init__  # noqa
from ..worker.celery_app import celery_app

@celery_app.task
def sync_account(account_id: int):
    # Stub for IMAP sync
    return {"synced": account_id}
