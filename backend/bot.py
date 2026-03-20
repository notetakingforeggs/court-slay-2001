import time
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from sqlalchemy.orm import Session
from models import Subscription
from database import SessionLocal

HELP_TEXT = """Welcome to Court Slay 2000!

/claimant: <name> — subscribe to alerts for a claimant
/defendant: <name> — subscribe to alerts for a defendant
/view — see your current subscriptions
/clear — remove your subscriptions
"""


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.strip()
    lower = text.lower()

    db: Session = SessionLocal()
    try:
        if lower.startswith("/claimant:"):
            name = text[len("/claimant:"):].strip()
            if not name:
                await update.message.reply_text("Usage: /claimant: <name>")
                return
            sub = db.query(Subscription).filter_by(chat_id=chat_id).first()
            if not sub:
                sub = Subscription(chat_id=chat_id, alert_terms_claimant=[], alert_terms_defendant=[], last_notified_timestamp=int(time.time()))
                db.add(sub)
            sub.alert_terms_claimant = (sub.alert_terms_claimant or []) + [name]
            db.commit()
            await update.message.reply_text(f"Subscribed to claimant alerts for: {name}")

        elif lower.startswith("/defendant:"):
            name = text[len("/defendant:"):].strip()
            if not name:
                await update.message.reply_text("Usage: /defendant: <name>")
                return
            sub = db.query(Subscription).filter_by(chat_id=chat_id).first()
            if not sub:
                sub = Subscription(chat_id=chat_id, alert_terms_claimant=[], alert_terms_defendant=[], last_notified_timestamp=int(time.time()))
                db.add(sub)
            sub.alert_terms_defendant = (sub.alert_terms_defendant or []) + [name]
            db.commit()
            await update.message.reply_text(f"Subscribed to defendant alerts for: {name}")

        elif lower.startswith("/view"):
            sub = db.query(Subscription).filter_by(chat_id=chat_id).first()
            if not sub:
                await update.message.reply_text("You have no active subscriptions.")
                return
            lines = ["Your subscriptions:\n", "Claimants:"]
            for t in (sub.alert_terms_claimant or []):
                lines.append(f"  • {t}")
            lines.append("\nDefendants:")
            for t in (sub.alert_terms_defendant or []):
                lines.append(f"  • {t}")
            await update.message.reply_text("\n".join(lines))

        elif lower.startswith("/clear"):
            db.query(Subscription).filter_by(chat_id=chat_id).delete()
            db.commit()
            await update.message.reply_text("Your subscriptions have been cleared.")

        else:
            await update.message.reply_text(HELP_TEXT)

    finally:
        db.close()


def build_bot(token: str) -> Application:
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    return app
