from returns.result import Success
from flask import Blueprint, jsonify
from app.service.serivce_world_map import create_world_map
from app.service.service_part_one import (find_events_by_attack_type,
                                          find_events_by_casualties_group_name,
                                          find_avg_events_by_country,
                                          find_events_by_country_and_year,
                                          find_events_by_activity_group_and_country,
                                          find_events_by_activity_group_and_specific_country)

group_casualties_blueprint = Blueprint('groups', __name__)
event_attack_type_blueprint = Blueprint('attack', __name__)
avg_casualties_country_blueprint = Blueprint('country', __name__)


# שאלה 1
# http://localhost:5000/api/event_attack_type/
@event_attack_type_blueprint.route('/', methods=['GET'])
def get_event_by_attack_type():
    try:
        attacks = find_events_by_attack_type()
        if isinstance(attacks, Success):
            return jsonify({"attacks": attacks.value_or([])}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': {str(e)}}), 500


# שאלה 1 A
# http://localhost:5000/api/event_attack_type/top/5

@event_attack_type_blueprint.route('/top/<num>', methods=['GET'])
def get_top_event_by_attack_type(num):
    try:
        num = int(num)
        attacks = find_events_by_attack_type(num)
        if isinstance(attacks, Success):
            return jsonify({"attacks": attacks.value_or([])}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error fetching attack by type: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500





# שאלה 2
#צריך מפה
# http://localhost:5000/api/avg_casualties_country/

@avg_casualties_country_blueprint.route('/', methods=['GET'])
def get_all_countries():
    try:
        attacks = find_avg_events_by_country()
        print(attacks)
        if isinstance(attacks, Success):
            # return jsonify({"attacks": attacks.value_or([])}), 200
            return jsonify({"html":create_world_map(attacks.value_or([]))}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error fetching  country: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

#שאלה 2 A
# http://localhost:5000/api/avg_casualties_country/top-5/

@avg_casualties_country_blueprint.route('/top-5/', methods=['GET'])
def get_top_countries():
    try:
        attacks = find_avg_events_by_country(5)
        if isinstance(attacks, Success):
            # return jsonify({"attacks": attacks.value_or([])}), 200
            return jsonify({"html":create_world_map(attacks.value_or([]))}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error fetching  country: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500



#שאלה 3
# http://localhost:5000/api/group_casualties/

@group_casualties_blueprint.route('/', methods=['GET'])
def get_groups():
    try:
        attacks = find_events_by_casualties_group_name(5)
        if isinstance(attacks, Success):
            return jsonify({"attacks": attacks.value_or([])}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error fetching  group: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# שאלה 6 אחוז שינוי במספר הפיגועים בין שנים לפי אזור.
# http://localhost:5000/api/avg_casualties_country/year/

@avg_casualties_country_blueprint.route('/year/', methods=['GET'])
def get_events_by_country_and_year():
    try:
        attacks = find_events_by_country_and_year()
        if isinstance(attacks, Success):
            return jsonify({"html":create_world_map(attacks.value_or([]))}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error fetching top events: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# http://localhost:5000/api/avg_casualties_country/year/top_5/

@avg_casualties_country_blueprint.route('/year/top_5/', methods=['GET'])
def get_events_by_country_and_year_top_5():
    try:
        attacks = find_events_by_country_and_year(5)
        if isinstance(attacks, Success):
            return jsonify({"html":create_world_map(attacks.value_or([]))}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error fetching top events: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

#  שאלה 8 קבוצות הפעילות ביותר באזור מסוים
#צריך מפה 
# http://localhost:5000/api/group_casualties/activity_group/

@group_casualties_blueprint.route('/activity_group/', methods=['GET'])
def get_events_by_activity_group():
    try:
        attacks = find_events_by_activity_group_and_country()
        if isinstance(attacks, Success):
            # return jsonify({"attacks": attacks.value_or([])}), 200
            return jsonify({"html":create_world_map(attacks.value_or([]))}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error fetching top events: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

# http://localhost:5000/api/group_casualties/activity_group/United States/

@group_casualties_blueprint.route('/activity_group/<country>/', methods=['GET'])
def get_activity_group_by_country(country):
    try:
        print(country)
        attacks = find_events_by_activity_group_and_specific_country(country)
        print(attacks)
        if isinstance(attacks, Success):
            # return jsonify({"attacks": attacks.value_or([])}), 200
            return jsonify({"html":create_world_map(attacks.value_or([]))}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error fetching top events: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

