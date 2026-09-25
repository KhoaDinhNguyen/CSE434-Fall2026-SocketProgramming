import gzip
import csv

FIELD_NAMES = [
    "event_id",
    "state",
    "year",
    "month_name",
    "event_type",
    "cz_type",
    "cz_name",
    "injuries_direct",
    "injuries_indirect",
    "deaths_direct",
    "deaths_indirect",
    "damage_property",
    "damage_crops",
    "tor_f_scale",
]


class StormEvent:
    def __init__(self, values):
        for key, value in zip(FIELD_NAMES, values):
            setattr(self, key, value)

        self.event_id = int(self.event_id)

    def to_string(self):
        return ",".join(str(getattr(self, name)) for name in FIELD_NAMES)

    @classmethod
    def from_string(cls, text):
        return cls(text.split(","))


def load_storms_event(filepath):
    events = []

    with gzip.open(filepath, "rt", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            events.append(StormEvent(row))

    return events
