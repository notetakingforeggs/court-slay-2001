import time
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import CourtCase, Subscription
from database import SessionLocal


def format_hits(claimant_hits: list, defendant_hits: list) -> str:
    lines = ["»» New hits for your subscribed alerts ««\n"]

    if claimant_hits:
        lines.append("Claimant hits:")
        for c in claimant_hits:
            dt = datetime.fromtimestamp(c.start_time_epoch, tz=timezone.utc)
            lines.append(f"  • {dt.strftime('%d/%m/%Y %H:%M')} — {c.case_details}")

    if defendant_hits:
        lines.append("\nDefendant hits:")
        for c in defendant_hits:
            dt = datetime.fromtimestamp(c.start_time_epoch, tz=timezone.utc)
            lines.append(f"  • {dt.strftime('%d/%m/%Y %H:%M')} — {c.case_details}")

    return "\n".join(lines)


async def run_notifier(bot):
    db: Session = SessionLocal()
    try:
        for sub in db.query(Subscription).all():
            claimant_hits = []
            defendant_hits = []

            for term in (sub.alert_terms_claimant or []):
                claimant_hits += (
                    db.query(CourtCase)
                    .filter(
                        CourtCase.claimant.ilike(f"%{term}%"),
                        CourtCase.created_at > sub.last_notified_timestamp,
                    )
                    .all()
                )

            for term in (sub.alert_terms_defendant or []):
                defendant_hits += (
                    db.query(CourtCase)
                    .filter(
                        CourtCase.defendant.ilike(f"%{term}%"),
                        CourtCase.created_at > sub.last_notified_timestamp,
                    )
                    .all()
                )

            if claimant_hits or defendant_hits:
                await bot.send_message(
                    chat_id=sub.chat_id,
                    text=format_hits(claimant_hits, defendant_hits),
                )
                sub.last_notified_timestamp = int(time.time())
                db.commit()
    finally:
        db.close()
