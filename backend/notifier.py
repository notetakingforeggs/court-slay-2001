import time
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import CourtCase, Court, Subscription
from database import SessionLocal

logger = logging.getLogger("court-slay")

TELEGRAM_MAX = 4096


def format_case(c, court_name, label):
    dt = datetime.fromtimestamp(c.start_time_epoch, tz=timezone.utc)
    return (
        f"• {dt.strftime('%d/%m/%Y %H:%M')} — {court_name}\n"
        f"  {label}: {c.claimant if label == 'Claimant' else c.defendant}\n"
        f"  {c.case_details or '-'}"
    )


def split_messages(header, lines):
    """Yield message strings each within Telegram's 4096-char limit."""
    chunks = [header]
    current_len = len(header)

    for line in lines:
        # +1 for the newline separator
        if current_len + len(line) + 1 > TELEGRAM_MAX:
            yield "\n".join(chunks)
            chunks = [line]
            current_len = len(line)
        else:
            chunks.append(line)
            current_len += len(line) + 1

    if chunks:
        yield "\n".join(chunks)


async def run_notifier(bot):
    db: Session = SessionLocal()
    try:
        for sub in db.query(Subscription).all():
            lines = []

            now = int(time.time())

            for term in (sub.alert_terms_claimant or []):
                hits = (
                    db.query(CourtCase, Court.city)
                    .join(Court, CourtCase.court_id == Court.id)
                    .filter(
                        CourtCase.claimant.ilike(f"%{term}%"),
                        CourtCase.created_at > sub.last_notified_timestamp,
                        CourtCase.start_time_epoch >= now,
                    )
                    .all()
                )
                if hits:
                    lines.append(f"\nClaimant matches for '{term}':")
                    for case, city in hits:
                        lines.append(format_case(case, city, "Claimant"))

            for term in (sub.alert_terms_defendant or []):
                hits = (
                    db.query(CourtCase, Court.city)
                    .join(Court, CourtCase.court_id == Court.id)
                    .filter(
                        CourtCase.defendant.ilike(f"%{term}%"),
                        CourtCase.created_at > sub.last_notified_timestamp,
                        CourtCase.start_time_epoch >= now,
                    )
                    .all()
                )
                if hits:
                    lines.append(f"\nDefendant matches for '{term}':")
                    for case, city in hits:
                        lines.append(format_case(case, city, "Defendant"))

            if lines:
                header = "New hits for your subscribed alerts"
                sent = 0
                for msg in split_messages(header, lines):
                    await bot.send_message(chat_id=sub.chat_id, text=msg)
                    sent += 1
                logger.info(f"Notified chat {sub.chat_id} — {sent} message(s) sent")
                sub.last_notified_timestamp = int(time.time())
                db.commit()
    finally:
        db.close()
