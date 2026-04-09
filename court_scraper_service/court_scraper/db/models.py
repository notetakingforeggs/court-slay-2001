from dataclasses import dataclass,field
from typing import Optional
from court_scraper.utils.time_converter import convert_to_unix_timestamp

@dataclass
class CourtCase:
    case_id: str
    start_time_string: str
    date: str
    duration: int
    case_details: str
    claimant: str
    defendant: str
    is_minor: bool
    hearing_type: str
    hearing_channel: str
    city: str
    start_time_epoch: int  = field(init=False)
    judge_name: Optional[str] = None
    hearing_room: Optional[str] = None
        
    def __post_init__(self):
        self.start_time_epoch = convert_to_unix_timestamp(self.start_time_string, self.date)
        