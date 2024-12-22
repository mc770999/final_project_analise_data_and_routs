from flask import jsonify, Blueprint
from returns.result import Success
from app.service.serivce_world_map import create_world_map
from app.service.service_part_two import find_group_with_same_targets, find_group_same_target, \
    find_countries_with_same_kind, find_group_same_target_kind, find_region_with_high_activity_group

group_target_blueprint = Blueprint('group_target', __name__)

# שאלה 11
# מפה
# http://localhost:5000/api/group_target/group_with_same_targets/1/


types = {"1": "country", "2": "region"}


@group_target_blueprint.route('/group_with_same_targets/<_type>/', methods=['GET'])
def group_with_same_targets(_type):
    try:
        print(types.get(_type, "region"))
        attacks = find_group_with_same_targets(types.get(_type))
        if isinstance(attacks, Success):
            return jsonify({"html": create_world_map(attacks.value_or([]))}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': {str(e)}}), 500







# 13 . איתור קבוצות שהשתתפו באותן תקיפות. שאלה: אילו קבוצות טרור היו מעורבות באותה תקיפה?
# http://localhost:5000/api/group_target/group_same_target/


@group_target_blueprint.route('/group_same_target/', methods=['GET'])
def group_same_target():
    try:
        attacks = find_group_same_target()
        if isinstance(attacks, Success):
            return jsonify({"attacks": attacks.value_or([])}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error: {str(e)}")
        return (jsonify({'error': {str(e)}})), 500

# 14. זיהוי אזורים עם אסטרטגיות תקיפה משותפות בין קבוצות. שאלה: באילו אזורים קבוצות שונות
# משתמשות באותן סוגי התקפות
# .a
# country או region : אפשרות סינון איזור .b
# marker הצגת .c
# להראות את רשימת הקבוצות
# http://localhost:5000/api/group_target/countries_with_same_kind/1/

@group_target_blueprint.route('/countries_with_same_kind/<_type>/', methods=['GET'])
def countries_with_same_kind(_type):
    try:
        attacks = find_countries_with_same_kind(types[_type])
        if isinstance(attacks, Success):
            return jsonify({"html": create_world_map(attacks.value_or([]))}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': {str(e)}}), 500







# 15. איתור קבוצות עם העדפות דומות למטרות. שאלה: אילו קבוצות תוקפות באופן תדיר את אותם סוגי
# מטרות )למשל אזרחים, ממשלה(?
# http://localhost:5000/api/group_target/group_same_target_kind/

@group_target_blueprint.route('/group_same_target_kind/', methods=['GET'])
def group_same_target_kind():
    try:
        attacks = find_group_same_target_kind()
        if isinstance(attacks, Success):
            return jsonify({"attacks": attacks.value_or([])}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': {str(e)}}), 500

# שאלה 16
#  . זיהוי אזורים עם פעילות בין-קבוצתית גבוהה. שאלה: באילו אזורים קיימת פעילות של המספר הגדול
# ביותר של קבוצות שונות - מגוון קבוצות ולא אותן קבוצות? לוגיקה: ספירת קבוצות ייחודיות הפעילות
# בכל אזור.
# .a
# country או region : אפשרות סינון איזור .b
# marker הצגת .c
# marker- לחיצה על ה .d
# http://localhost:5000/api/group_target/region_with_high_activity_group/1/

@group_target_blueprint.route('/region_with_high_activity_group/<_type>/', methods=['GET'])
def region_with_high_activity_group(_type):
    try:
        attacks = find_region_with_high_activity_group(types[_type])
        if isinstance(attacks, Success):
            return jsonify({"html": create_world_map(attacks.value_or([]))}), 200
        raise Exception("Error from data base to get attacks")
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': {str(e)}}), 500
