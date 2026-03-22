import logging
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from court_scraper.scraper.session import login
from court_scraper.scraper.fetch import get_court_links_and_dates
from court_scraper.scraper.court_scraper import CourtScraper
from court_scraper.db.db_methods import get_connection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("scraper")


def main():
    logger.info("Scrape starting")

    links_and_dates = get_court_links_and_dates()
    session = login()
    get_connection()

    court_scraper = CourtScraper(session, links_and_dates)
    court_scraper.run()

    logger.info("Scrape complete")


if __name__ == "__main__":
    logger.info("Scraper service starting — scheduled daily at 01:00")
    main()  # run once immediately on startup

    scheduler = BlockingScheduler()
    scheduler.add_job(main, "cron", hour=1, minute=0)
    scheduler.start()