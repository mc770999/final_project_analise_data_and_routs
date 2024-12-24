query_find_events_by_attack_type = ([
        {
            "$match": {
                "location.region": {"$ne": "[]"}
            }
        },
        {"$unwind": "$attack_type"},
        {
            "$group": {
                "_id": "$attack_type",
                "total_number_of_casualties_calc": {"$sum": "$number_of_casualties_calc"},
                "count_events": {"$sum": 1},
                "sample_events": {
                    "$push": {"event_id": "$event_id",
                              "num_kill": "$num_kill",
                              "num_wound": "$num_wound",
                              "number_of_casualties_calc": "$number_of_casualties_calc",
                              "date": "$date",
                              "location": "$location"
                              }}
            }
        },
        {"$sort": {"total_number_of_casualties_calc": -1}}
    ])

query_find_avg_events_by_country = [
            {
                "$match": {
                    "location.country": {"$ne": None},
                    "location.latitude": {"$ne": None},
                    "location.longitude": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": "$location.country",
                    "total_number_of_casualties_calc": {"$avg": "$number_of_casualties_calc"},
                    "latitude": {"$first": "$location.latitude"},
                    "longitude": {"$first": "$location.longitude"},
                    "count_events": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "country": "$_id",
                    "total_number_of_casualties_calc": 1,
                    "count_events": 1,
                    "location": {
                        "latitude": "$latitude",
                        "longitude": "$longitude"
                    }
                }
            },
            {
                "$sort": {"total_number_of_casualties_calc": -1}
            }
        ]

query_find_events_by_casualties_group_name = [
    {
        "$match": {
            "$and": [
                {"group_name": {"$ne": "[]"}},
            ]
        }
    },
    {"$unwind": "$group_name"},
    {
        "$group": {
            "_id": {
                "group_name": "$group_name"
            },
            "count_events": {"$sum": 1},
            "count_casualties": {"$sum": "$number_of_casualties_calc"},
            "latitude": {"$first": "$location.latitude"},
            "longitude": {"$first": "$location.longitude"},
        }
    },
    {
        "$project": {
            "region": "$_id.region",
            "group_name": "$_id.group_name",
            "count_events": 1,
            "count_casualties": 1,
            "location": {
                "latitude": "$latitude",
                "longitude": "$longitude"
            },
            "_id": 0
        }
    },
    {"$sort": {"count_casualties": -1}}
]

query_find_events_by_country_and_year = [
    {
        "$match": {
            "location.country": {"$ne": None},
            "group_name": {'$ne': []},
            "location.latitude": {"$ne": None},
            "location.longitude": {"$ne": None}
        }
    },
    {
        "$group": {
            "_id": {
                "country": "$location.country",
                "year": "$date.year"
            },
            "sum_events": {"$sum": 1},
            "latitude": {"$first": "$location.latitude"},
            "longitude": {"$first": "$location.longitude"},
        }
    },
    {
        "$sort": {
            "_id.country": 1,
            "_id.year": 1
        }
    },
    {
        "$group": {
            "_id": "$_id.country",
            "first_year_sum_events": {"$first": {"year": "$_id.year", "sum_events": "$sum_events"}},
            "last_year_sum_events": {"$last": {"year": "$_id.year", "sum_events": "$sum_events"}},
            "latitude": {"$first": "$latitude"},
            "longitude": {"$first": "$longitude"},
        }
    },
    {
        "$project": {
            "country": "$_id",
            "first_year_sum_events": 1,
            "last_year_sum_events": 1,
            "location": {
                "latitude": "$latitude",
                "longitude": "$longitude"
            },
            "_id": 0
        }
    }
]

query_find_events_by_activity_group_and_country = [
    {
        "$match": {
            "group_name": {'$ne': []},
            "location.country": {"$ne": None},
            "location.latitude": {"$ne": None},
            "location.longitude": {"$ne": None}
        }
    },
    {"$unwind": "$group_name"},
    {
        "$group": {
            "_id": {
                "group": "$group_name",
                "country": "$location.country",
            },
            "sum_events": {"$sum": 1},
            "count_casualties": {"$sum": "$number_of_casualties_calc"},
            "latitude": {"$first": "$location.latitude"},
            "longitude": {"$first": "$location.longitude"},
        }
    },
    {
        "$project": {
            "group": "$_id.group",
            "country": "$_id.country",
            "sum_events": 1,
            "count_casualties": 1,
            "location": {
                "latitude": "$latitude",
                "longitude": "$longitude"
            },
            "_id": 0
        }
    },
    {"$sort": {"sum_events": -1}},
    {
        "$limit": 5
    }
]

query_find_events_by_activity_group_and_specific_country = lambda country :[
{
            "$match": {
                "location.country": {"$regex": f"^{country}$", "$options": "i"},
                "group_name": {'$ne': []},
                "location.latitude": {"$ne": None},
                "location.longitude": {"$ne": None}
            }
        },
    {"$unwind": "$group_name"},
    {
        "$group": {
            "_id": {
                "country": "$location.country",
                "group": "$group_name"
            },
            "sum_events": {"$sum": 1},
            "count_casualties": {"$sum": "$number_of_casualties_calc"},
            "latitude": {"$first": "$location.latitude"},
            "longitude": {"$first": "$location.longitude"}
        }
    },
    {
        "$project": {
            "country": "$_id.country",
            "group": "$_id.group",
            "sum_events": 1,
            "count_casualties": 1,
            "location": {
                "latitude": "$latitude",
                "longitude": "$longitude"
            },
            "_id": 0
        }
    },
    {"$sort": {"count_casualties": -1}},
    {
        "$limit": 5
    }
]

query_find_group_with_same_targets = lambda _type: [
        # Step 1: Filter by region or country, and ensure non-empty group names
        {
            "$match": {
                "$and": [
                    {f"location.{_type}": {"$ne": None}},  # Ensure the location of the given type is not null
                    {"group_name": {"$ne": []}},
                    {"target_types": {"$ne": []}},
                    {"location.latitude": {"$ne": None}},
                    {"location.longitude": {"$ne": None}}
                ]
            }
        },
        # Step 2: Unwind target _types and group names
        {"$unwind": "$target_types"},
        {"$unwind": "$group_name"},
        # Step 3: Group by country and target _type, collecting unique groups
        {
            "$group": {
                "_id": {
                    f"{_type}": f"$location.{_type}",  # Use the dynamic key in the group
                    "target": "$target_types.target"
                },
                "groups": {"$addToSet": "$group_name"},
                "latitude": {"$first": "$location.latitude"},
                "longitude": {"$first": "$location.longitude"}
                # Collect unique group names
            }
        },
        # Step 4: Filter for targets with multiple groups
        {
            "$match": {
                "groups.1": {"$exists": True}  # Ensure at least two groups
            }
        },
        # Step 5: Format the output
        {
            "$project": {
                _type: f"$_id.{_type}",  # Properly map the dynamic key for _type
                "target": "$_id.target",
                "groups": 1,
                "location": {
                    "latitude": "$latitude",
                    "longitude": "$longitude"
                },
                "_id": 0  # Exclude _id from the final result
            }
        }
    ]

query_find_group_same_target = [
    {
        "$match": {
            "group_name.1": {"$exists": True}
        }
    },
    {
        "$project": {
            "_id": 0,
            "event_id": 1,
            "groups": "$group_name",
            "location": "$location",
            "date": "$date",
            "summary": "$summary"
        }
    }
]

query_find_countries_with_same_kind = lambda _type: [
        {
            "$match": {
                    "location.latitude": {"$ne": None},
                    "location.longitude": {"$ne": None},
                    f"location.{_type}": {"$ne": None}
            }
        },
        {
            "$unwind": "$attack_type"
        },
        {
            "$unwind": "$group_name"
        },
        {
            "$group": {
                "_id": {
                    _type: f"$location.{_type}",
                    "attack_type": "$attack_type"
                },
                "groups": {"$addToSet": "$group_name"},
                "count_casualties": {"$sum": "$number_of_casualties_calc"},
                "latitude": {"$first": "$location.latitude"},
                "longitude": {"$first": "$location.longitude"}
            }
        },
        {
            "$match": {
                "groups.1": {"$exists": True}
            }
        },
        {
            "$project": {
                "_id": 0,
                _type: f"$_id.{_type}",
                "attack_type": "$_id.attack_type",
                "groups": 1,
                "location": {
                    "latitude": "$latitude",
                    "longitude": "$longitude"
                },
                "count_casualties":1
            }
        }
    ]

query_find_group_same_target_kind = [
    {
        "$match": {
            "location.latitude": {"$ne": None},
            "location.longitude": {"$ne": None}
        }
    },
    {
        "$unwind": "$target_types"
    },
    {
        "$unwind": "$group_name"
    },
    {
        "$group": {
            "_id": "$target_types.target_type",
            "groups": {"$addToSet": "$group_name"},
            "count": {"$sum": 1}
        }
    },
    {
        "$match": {
            "groups.1": {"$exists": True}
        }
    },
    {
        "$project": {
            "_id": 0,
            "target_type": "$_id",
            "groups": 1,
            "attack_count": "$count",
            "location": {
                "latitude": "$latitude",
                "longitude": "$longitude"
            },
        }
    },
    {
        "$sort": {
            "attack_count": -1
        }
    }
]

query_find_region_with_high_activity_group = lambda _type: [
    {
        "$match": {
            f"location.{_type}": {"$ne": None},
            "location.latitude": {"$ne": None},
            "location.longitude": {"$ne": None}
        }
    },
    {
        "$unwind": "$group_name"
    },
    {
        "$group": {
            "_id": {
                _type: f"$location.{_type}"
            },
            "uniqueGroups": {"$addToSet": "$group_name"},
            "latitude": {"$first": "$location.latitude"},
            "longitude": {"$first": "$location.longitude"}
        }
    },
    {
        "$project": {
            "_id": 0,
            _type: f"$_id.{_type}",
            "uniqueGroupCount": {"$size": "$uniqueGroups"},
            "location": {
                "latitude": "$latitude",
                "longitude": "$longitude"
            },
        }
    },
    {
        "$sort": {
            "uniqueGroupCount": -1
        }
    }
]

