import logging
from court_scraper.scraper.clients.court_client import CourtClient
from court_scraper.scraper.parsers.entry_page_parser import EntryPageParser
from court_scraper.db.db_methods import get_court_id_by_city, insert_court_case
from court_scraper.scraper.session import BASE_URL
from court_scraper.scraper.flavours import flavours

logger = logging.getLogger("scraper.court")

CASE_LIST_BASE_URL = "https://www.courtserve.net/courtlists/viewcourtlistv2.php"

class CourtScraper:
    def __init__(self, session, links_and_dates):

        self.session = session
        self.links_and_dates = links_and_dates
        self.new_tab_url = None
        self.city = None
        self.court_name = None # am i just going to collapse city and court name? so far unused i think
        self.case_rows = None
        self.case_soup = None

        self.court_client = CourtClient(self.session, BASE_URL)

    # passing session from main where it is returned from the session/login call. BASE URL in main also?
    def run(self):
        total_new = 0

        for i, (link, date) in enumerate(self.links_and_dates):
            if i < 1:
                continue

            entry_page_response_text = self.court_client.fetch_entry_page(link)
            entry_page_parser = EntryPageParser(entry_page_response_text)
            new_tab_url = entry_page_parser.parse_for_new_tab_url()

            case_list_response_text = self.court_client.fetch_case_list(CASE_LIST_BASE_URL + new_tab_url)
            flavour = flavours.detect_Flavour(case_list_response_text)
            court_list_parser = flavour.parser_class(case_list_response_text)

            self.city = court_list_parser.extract_city()
            row_texts_messy = court_list_parser.extract_case_rows()
            court_case_factory = flavour.factory_class(row_texts_messy, date, self.city)
            court_cases = court_case_factory.process_rows_to_cases()

            try:
                if not court_cases:
                    logger.warning(f"No cases extracted for: {self.city}")
                    continue

                court_new = 0
                for case in court_cases:
                    court_id = get_court_id_by_city(case.city)
                    if not court_id and case.city:
                        logger.warning(f"No court ID found for city: {case.city}")
                        continue
                    if insert_court_case(case, court_id):
                        court_new += 1

                total_new += court_new
                logger.info(f"{self.city}: {court_new} new / {len(court_cases)} total")

            except Exception as e:
                logger.error(f"Failed scraping {self.city}: {e}")

        return total_new

     
