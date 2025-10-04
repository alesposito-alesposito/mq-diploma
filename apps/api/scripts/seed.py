from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import random

from app.models import Base, User, Account, Thread, Message, Note
from app.config import settings

engine = create_engine(settings.database_url, future=True)

SUBJECTS = [
    "Welcome to Notion Mail",
    "Your weekly newsletter",
    "Meeting notes",
    "Invoice #12345",
    "GitHub notifications",
]
BODIES = [
    "This is a demo email body with some content.",
    "Another message body for testing the thread list.",
    "Here are the details you requested.",
]

def run():
    with Session(engine) as db:
        # Create demo user and account if not exists
        user = db.query(User).filter(User.email == "demo@example.com").first()
        if not user:
            user = User(email="demo@example.com", name="Demo User")
            db.add(user)
            db.flush()
        account = db.query(Account).filter(Account.user_id == user.id).first()
        if not account:
            account = Account(user_id=user.id, provider="demo", email="demo@example.com", created_at=datetime.utcnow())
            db.add(account)
            db.flush()
        # Seed 5 threads with messages
        now = datetime.utcnow()
        for i in range(5):
            thread = Thread(
                account_id=account.id,
                subject=random.choice(SUBJECTS),
                last_message_at=now - timedelta(hours=i),
                participants=["alice@example.com", "bob@example.com"],
                unread_count=random.randint(0, 3),
                folder="INBOX",
                tags=["people"],
            )
            db.add(thread)
            db.flush()
            for j in range(random.randint(1, 3)):
                msg = Message(
                    account_id=account.id,
                    thread_id=thread.id,
                    subject=thread.subject,
                    from_addr="alice@example.com",
                    to_addrs="demo@example.com",
                    date=thread.last_message_at - timedelta(minutes=j),
                    snippet="Snippet for message",
                    body_text=random.choice(BODIES),
                    has_attachments=False,
                    folder="INBOX",
                    created_at=thread.last_message_at - timedelta(minutes=j),
                )
                db.add(msg)
            note = Note(thread_id=thread.id, author_user_id=user.id, blocks_json={"type": "doc", "content": [{"type": "paragraph", "text": "Demo note"}]}, created_at=now, updated_at=now)
            db.add(note)
        db.commit()
        print("Seed completed")

if __name__ == "__main__":
    run()
