from returns.result import Success, Failure
from app.queries.mongo_queries import query_find_events_by_attack_type, \
    query_find_avg_events_by_country, query_find_events_by_casualties_group_name, query_find_events_by_country_and_year, \
    query_find_events_by_activity_group_and_country, query_find_events_by_activity_group_and_specific_country
from app.utils.country_service import calculate_percent_change
from ..db.mongo_database import event_collection


# שאלה 1
def find_events_by_attack_type(num=None):
    attacks = list(event_collection.aggregate(query_find_events_by_attack_type))[:num]
    if attacks:
        return Success(attacks)
    else:
        return Failure("find attacks failed.")


# שאלה 2
def find_avg_events_by_country(num=None):
    try:
        attacks = list(event_collection.aggregate(query_find_avg_events_by_country))
        print(attacks)
        if attacks:
            return Success(attacks[:num])
        else:
            return Failure("No events found.")
    except Exception as e:
        print(f"Error occurred: {e}")
        return Failure("An error occurred while finding events by region.")


# שאלה 3
def find_events_by_casualties_group_name(num=None):

    attacks = list(event_collection.aggregate(query_find_events_by_casualties_group_name))[:num]
    if attacks:
        return Success(attacks)
    else:
        return Failure("find attacks failed.")


# שאלה 6
def find_events_by_country_and_year(num=None):
    try:
        attacks = list(event_collection.aggregate(query_find_events_by_country_and_year))
        print(attacks)
        if attacks:
            return Success([{**att, "percent_change": calculate_percent_change(att)} for att in attacks[:num]])
        else:
            return Failure("find attacks failed.")
    except Exception as e:
        print(e)


# שאלה 8
def find_events_by_activity_group_and_country(num=None):
    try:
        attacks = list(event_collection.aggregate(query_find_events_by_activity_group_and_country))
        if attacks:
            return Success(attacks[:num])
        else:
            return Failure("find attacks failed.")
    except Exception as e:
        print(e)


# a שאלה 8
def find_events_by_activity_group_and_specific_country(country, num=None):
    try:
        attacks = list(event_collection.aggregate(query_find_events_by_activity_group_and_specific_country(country)))
        if attacks:
            return Success(attacks[:num])
        else:
            return Failure("find attacks failed.")
    except Exception as e:
        return e
