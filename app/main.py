from flask import Flask
from flask_cors import CORS
from app.routs.controller_part_two import group_target_blueprint
from app.routs.search_controller import search_blueprint
from app.routs.controller_part_one import (event_attack_type_blueprint,
                                           avg_casualties_country_blueprint,
                                           group_casualties_blueprint)

app = Flask(__name__)

CORS(app)

app.register_blueprint(event_attack_type_blueprint, url_prefix="/api/event_attack_type")
app.register_blueprint(avg_casualties_country_blueprint, url_prefix="/api/avg_casualties_country")
app.register_blueprint(group_casualties_blueprint, url_prefix="/api/group_casualties")
app.register_blueprint(group_target_blueprint, url_prefix="/api/group_target")
app.register_blueprint(search_blueprint, url_prefix="/api/search")

if __name__ == '__main__':

    app.run()

