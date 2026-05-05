from datetime import date, timedelta

from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.exceptions import SourceArgumentNotFound

TITLE = "City of Bunbury"
DESCRIPTION = "Source for City of Bunbury (WA) waste collection."
URL = "https://www.bunbury.wa.gov.au"
COUNTRY = "au"
TEST_CASES = {
    "Monday collection, recycling even weeks": {
        "collection_day": "Monday",
        "recycling_in_even_week": True,
    },
    "Wednesday collection, recycling odd weeks": {
        "collection_day": "Wednesday",
        "recycling_in_even_week": False,
    },
    "Friday collection": {
        "collection_day": "Friday",
        "recycling_in_even_week": True,
    },
}

ICON_MAP = {
    "FOGO": "mdi:leaf",
    "Recycling": "mdi:recycle",
    "Landfill": "mdi:trash-can",
}

HOW_TO_GET_ARGUMENTS_DESCRIPTION = {
    "en": (
        "Download the Waste Calendar from https://www.bunbury.wa.gov.au/live/"
        "waste-services/waste-collections (or use the City of Bunbury My 3 Bins "
        "app) to find your collection day. The calendar map shows Monday–Friday "
        "zones across the city. "
        "For recycling_in_even_week: check your last recycling collection date "
        "and see if its ISO week number (https://whatweekisit.org/) was even "
        "(True) or odd (False)."
    ),
}

PARAM_DESCRIPTIONS = {
    "en": {
        "collection_day": (
            "Your bin collection day: 'Monday', 'Tuesday', 'Wednesday', "
            "'Thursday', or 'Friday'. Check the Waste Calendar PDF or "
            "My 3 Bins app on the City of Bunbury website."
        ),
        "recycling_in_even_week": (
            "Set to True if your recycling bin is collected on even ISO week "
            "numbers, False if on odd ISO week numbers. Check your last recycling "
            "collection date to determine this."
        ),
    },
}

PARAM_TRANSLATIONS = {
    "en": {
        "collection_day": "Collection Day",
        "recycling_in_even_week": "Recycling collected on even ISO weeks",
    },
}

DAY_NAME_TO_WEEKDAY = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
}


def _next_weekday(ref: date, weekday: int) -> date:
    days_ahead = weekday - ref.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return ref + timedelta(days=days_ahead)


class Source:
    def __init__(self, collection_day: str, recycling_in_even_week: bool = True):
        self._collection_day = collection_day.strip().lower()
        self._recycling_in_even_week = recycling_in_even_week

        if self._collection_day not in DAY_NAME_TO_WEEKDAY:
            raise SourceArgumentNotFound(
                "collection_day",
                f"'{collection_day}' is not valid. "
                f"Use one of: {', '.join(d.capitalize() for d in DAY_NAME_TO_WEEKDAY)}.",
            )

    def fetch(self) -> list[Collection]:
        weekday = DAY_NAME_TO_WEEKDAY[self._collection_day]
        entries: list[Collection] = []
        today = date.today()
        first_day = _next_weekday(today, weekday)

        for week in range(26):
            d = first_day + timedelta(weeks=week)
            iso_week = d.isocalendar()[1]
            even_week = iso_week % 2 == 0

            # FOGO collected every week
            entries.append(Collection(date=d, t="FOGO", icon=ICON_MAP["FOGO"]))

            # Recycling and Landfill alternate fortnightly
            if even_week == self._recycling_in_even_week:
                entries.append(
                    Collection(date=d, t="Recycling", icon=ICON_MAP["Recycling"])
                )
            else:
                entries.append(
                    Collection(date=d, t="Landfill", icon=ICON_MAP["Landfill"])
                )

        return entries
