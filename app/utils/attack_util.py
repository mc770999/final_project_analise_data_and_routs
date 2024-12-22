from mongo_db.models.date_model import Date
from mongo_db.models.event_model import Event
from mongo_db.models.location_model import Location
from mongo_db.models.target_type_model import TargetType


def convert_to_event(event_json):
    location = Location(**event_json["location"])
    date = Date(**event_json["date"])
    target_types = [TargetType(**t) for t in event_json["target_types"]]
    event = Event(
        event_id=event_json['event_id'],
        num_kill=event_json['num_kill'],
        num_wound=event_json['num_wound'],
        number_of_casualties_calc=event_json['number_of_casualties_calc'],
        date=date,
        summary=event_json["summary"],
        num_preps=event_json["num_preps"],
        location=location,
        attack_type=event_json["attack_type"],
        target_types=target_types,
        group_name=event_json["group_name"]
    )
    return event
