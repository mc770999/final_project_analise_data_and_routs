from flask import Flask, request, jsonify, Blueprint
from app.service.serivce_world_map import (create_world_map)
from app.service.service_search import search_by_keywords, search_by_keywords_and_index, \
    search_keyword_in_all_indexes_between_dates


search_blueprint = Blueprint('search', __name__)

# http://localhost:5000//api/search/keywords/

@search_blueprint.route('/keywords/<query>/<limit>/', methods=['GET'])
def search_keywords(query, limit):
    try:
        limit = int(limit) if limit else 10  # Default limit to 10 if not provided
        list_keywords = query.split(",")
        print(limit, list_keywords)
        events = search_by_keywords(list_keywords, limit)  # Search for events using the list of keywords and limit

        return jsonify({"html": create_world_map(events.value_or([]))}), 200
    except Exception as e:
        return jsonify({"failure": e}), 200


# http://localhost:5000/api/search/news/

@search_blueprint.route('/news/<query>/<limit>/', methods=['GET'])
def search_news(query, limit):
    try:
        limit = int(limit) if limit else 10

        list_keywords = query.split(",")
        events = search_by_keywords_and_index("nowadays_terror_attack", list_keywords, limit)

        return jsonify({"html": create_world_map(events.value_or([]))}), 200
    except Exception as e:
        return jsonify({"failure": e}), 200

# http://localhost:5000/api/search/historic/

@search_blueprint.route('/historic/<query>/<limit>/', methods=['GET'])
def search_historic(query, limit):
    try:
        limit = int(limit) if limit else 10
        list_keywords = query.split(",")
        events = search_by_keywords_and_index("historical_terror_attack", list_keywords, limit)

        return jsonify({"html": create_world_map(events.value_or([]))}), 200
    except Exception as e:
        return jsonify({"failure": e}), 200

# http://localhost:5000/api/search/combined/

@search_blueprint.route('/combined/<query>/<limit>/', methods=['GET'])
def search_combined(query, limit):
    try:
        limit = int(limit) if limit else 10

        list_data = query.split("_")
        dates = list_data[1].split(",")
        list_keywords = list_data[0].split(",")
        events = search_keyword_in_all_indexes_between_dates(list_keywords, dates[0], dates[1], limit)

        return jsonify({"html": create_world_map(events.value_or([]))}), 200
    except Exception as e:
        return jsonify({"failure": e}), 200
