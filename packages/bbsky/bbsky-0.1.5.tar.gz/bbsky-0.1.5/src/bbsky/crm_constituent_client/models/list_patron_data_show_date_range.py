from enum import Enum


class ListPatronDataShowDateRange(str, Enum):
    ALL = "All"
    LAST_12_MONTHS = "Last 12 months"
    LAST_30_DAYS = "Last 30 days"
    LAST_90_DAYS = "Last 90 days"

    def __str__(self) -> str:
        return str(self.value)
