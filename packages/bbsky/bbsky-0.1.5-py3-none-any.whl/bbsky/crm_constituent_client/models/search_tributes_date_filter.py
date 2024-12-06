from enum import Enum


class SearchTributesDateFilter(str, Enum):
    THIS_MONTH = "This month"
    THIS_QUARTER = "This quarter"
    THIS_WEEK = "This week"
    THIS_YEAR = "This year"

    def __str__(self) -> str:
        return str(self.value)
