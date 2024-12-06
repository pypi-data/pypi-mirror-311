from enum import Enum


class SearchEducationsConstituencyStatus(str, Enum):
    ALL_STATUSES = "All statuses"
    CURRENTLY_ATTENDING = "Currently attending"
    GRADUATED = "Graduated"
    INCOMPLETE = "Incomplete"
    UNKNOWN = "Unknown"

    def __str__(self) -> str:
        return str(self.value)
