from enum import Enum


class ListTributesSiteFilterMode(str, Enum):
    ALL_SITES = "All sites"
    MY_SITE = "My site"
    MY_SITES_BRANCH = "My site's branch"
    SELECTED_SITES = "Selected sites"

    def __str__(self) -> str:
        return str(self.value)
