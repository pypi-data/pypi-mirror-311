from enum import Enum


class ListConstituentSolicitCodesDateRange(str, Enum):
    ALL_DATES = "All dates"
    LAST_2_YEARS = "Last 2 years"
    LAST_30_DAYS = "Last 30 days"
    LAST_60_DAYS = "Last 60 days"
    LAST_6_MONTHS = "Last 6 months"
    LAST_90_DAYS = "Last 90 days"
    LAST_YEAR = "Last year"

    def __str__(self) -> str:
        return str(self.value)
