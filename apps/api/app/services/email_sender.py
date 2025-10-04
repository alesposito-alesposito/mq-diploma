from typing import List, Optional
import aiosmtplib

async def send_email(
    account_id: int,
    to: List[str],
    cc: List[str],
    bcc: List[str],
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
):
    # Minimal stub: send via localhost relay or dev null
    # For MVP in docker, we no-op to avoid external SMTP
    return True
