import logging
from court_scraper.scraper.parsers.base import BaseDailyCauseListParser
import re

logger = logging.getLogger("scraper.parser")


class Flavour1DailyCauseListParser(BaseDailyCauseListParser):

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
            spans = row.find_all("span")
            span_texts = [span.text.strip() for span in spans]

            has_am_pm = any(re.search(am_pm_pattern, t) for t in span_texts)

            judge_text = next((t for t in span_texts if t.lower().startswith("before:")), None)
            if judge_text:
                current_judge = judge_text[len("before:"):].strip()
                continue

            if has_am_pm:
                results.append((span_texts, current_judge, current_room))
            else:
                # A room header row has exactly one real span (room name only).
                # Column header rows have multiple spans (Start Time, Duration, etc.)
                real_texts = [t for t in span_texts if t.replace('\xa0', '').strip()]
                if len(real_texts) == 1:
                    current_room = real_texts[0]

        logger.debug(f"{self.city}: has the following no of rows selected for (pre-cases): {len(results)}")
        return results
