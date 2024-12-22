from returns.result import Success, Failure
from ..db.mongo_database import event_collection
from ..queries.mongo_queries import query_find_group_with_same_targets, query_find_countries_with_same_kind, \
    query_find_group_same_target, query_find_group_same_target_kind, query_find_region_with_high_activity_group


def find_group_with_same_targets(_type):
    try:
        attacks = list(event_collection.aggregate(query_find_group_with_same_targets(_type)))
        if attacks:
            # Convert the 'groups' set to a list to avoid JSON serialization issues
            return Success(
                [{**att, "groups": list(att["groups"])} for att in attacks])
        else:
            return Failure("Find attacks failed. No results found.")
    except Exception as e:
        print(f"Error during aggregation: {e}")
        return Failure(f"An error occurred: {str(e)}")

# 13 . איתור קבוצות שהשתתפו באותן תקיפות. שאלה: אילו קבוצות טרור היו מעורבות באותה תקיפה?
def find_group_same_target():
    try:
        attacks = list(event_collection.aggregate(query_find_group_same_target))
        if attacks:
            return Success(attacks)
        else:
            return Failure("find attacks failed.")
    except Exception as e:
        print(e)


# 14. זיהוי אזורים עם אסטרטגיות תקיפה משותפות בין קבוצות. שאלה: באילו אזורים קבוצות שונות
def find_countries_with_same_kind(_type):
    try:
        attacks = list(event_collection.aggregate(query_find_countries_with_same_kind(_type)))
        print(attacks)

        if attacks:
            return Success(attacks)
        else:
            return Failure("find attacks failed.")
    except Exception as e:
        print(e)


def find_group_same_target_kind():
    try:
        attacks = list(event_collection.aggregate(query_find_group_same_target_kind))
        if attacks:
            return Success(attacks)
        else:
            return Failure("find attacks failed.")
    except Exception as e:
        print(e)


# שאלה 16
def find_region_with_high_activity_group(_type):
    try:
        attacks = list(event_collection.aggregate(query_find_region_with_high_activity_group(_type)))
        if attacks:
            return Success(attacks)
        else:
            return Failure("find attacks failed.")
    except Exception as e:
        print(e)
