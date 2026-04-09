import logging
from court_scraper.utils import time_converter
from court_scraper.scraper.parsers.base import BaseDailyCauseListParser
import re

logger = logging.getLogger("scraper.parser")


class Flavour2DailyCauseListParser(BaseDailyCauseListParser):

    def __init__(self, html):
        super().__init__(html)

    def extract_case_rows(self) -> list[tuple[list[str], str | None, str | None]]:
        '''Extract all text from td cells in rows that have court cases in .'''

        rows = self.case_soup.find_all("tr")
        results = []
        current_judge = None
        current_room = None
        am_pm_pattern = r"\bAM|PM\b|\dam\b|\dpm\b"

        for row in rows:
            if row.find("tr"):  # ignore rows that contain other rows
                continue

            b_tags = row.find_all("b")
            b_texts = [b.text.strip() for b in b_tags]

            has_am_pm = any(re.search(am_pm_pattern, t) for t in b_texts)

            # Judge and room may appear in the same row — extract both before deciding
            judge_text = next((t for t in b_texts if t.lower().startswith("before:")), None)
            room_text = next((t for t in b_texts if t.lower().startswith("courtroom:")), None)

            if judge_text:
                current_judge = judge_text[len("before:"):].strip()
            if room_text:
                current_room = room_text[len("courtroom:"):].strip()

            if judge_text or room_text:
                continue

            if has_am_pm:
                td_tags = row.find_all("td")
                texts = [
                    td.get_text(separator=" ", strip=True) for td in td_tags
                ]
                (start_time, duration) = time_converter.calculate_duration(texts[0])
                texts[0] = start_time
                texts.insert(1, duration)
                results.append((texts, current_judge, current_room))

        logger.debug(f"{self.city}: has the following no of rows selected for (pre-cases): {len(results)} - printing from flavour 2 dclp")
        return results
