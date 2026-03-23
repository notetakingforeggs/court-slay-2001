from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()

import os
import logging
from typing import Optional
from fastapi import FastAPI, Depends, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("court-slay")

# suppress noisy third party loggers
for noisy in ["httpx", "httpx._client", "httpcore", "httpcore.connection", "httpcore.http11", "telegram", "telegram.ext", "apscheduler", "apscheduler.scheduler", "apscheduler.executors.default", "uvicorn.access"]:
    logging.getLogger(noisy).setLevel(logging.WARNING)

from database import get_db
from models import CourtCase, Court, Region
from bot import build_bot
from notifier import run_notifier


scheduler = AsyncIOScheduler()
ptb_app = build_bot(os.getenv("BOT_TOKEN"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Court Slay 2000")

    logger.info("Starting Telegram bot")
    await ptb_app.initialize()
    await ptb_app.start()
    await ptb_app.updater.start_polling()

    logger.info("Starting scheduler — notifier runs daily at 07:30")
    scheduler.add_job(run_notifier, "cron", hour=7, minute=30, args=[ptb_app.bot])
    scheduler.start()

    yield

    logger.info("Shutting down")
    await ptb_app.updater.stop()
    await ptb_app.stop()
    await ptb_app.shutdown()
    scheduler.shutdown()


app = FastAPI(title="Court Slay 2000", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/cases")
def search_cases(
    claimant: Optional[str] = Query(None),
    defendant: Optional[str] = Query(None),
    hearing_type: Optional[str] = Query(None),
    court_id: Optional[int] = Query(None),
    region_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(CourtCase)
    if claimant:
        q = q.filter(CourtCase.claimant.ilike(f"%{claimant}%"))
    if defendant:
        q = q.filter(CourtCase.defendant.ilike(f"%{defendant}%"))
    if hearing_type:
        q = q.filter(CourtCase.hearing_type.ilike(f"%{hearing_type}%"))
    if court_id:
        q = q.filter(CourtCase.court_id == court_id)
    if region_id:
        q = q.join(Court).filter(Court.region_id == region_id)
    return q.limit(100).all()


@app.get("/courts")
def list_courts(db: Session = Depends(get_db)):
    return db.query(Court).all()


@app.get("/regions")
def list_regions(db: Session = Depends(get_db)):
    return db.query(Region).all()
