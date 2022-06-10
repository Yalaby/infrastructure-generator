from config import *
import src.classes as classes
import src.parsing_module as pm
import src.directory_check as dc
import src.dockerfile_processor as dp
import src.docker_compose_processor as dcp
import src.server_processor as sp
from flask import Flask, request, jsonify, abort
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/dockerfiles', methods=['POST'])
def dockerfile_creator():
    sd = request.get_json()
    try:
        dc.semantic_data_content_check(sd, CLIENTS_TEMPLATES_PATH, GATEWAYS_TEMPLATES_PATH,
                                       SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)
    except Exception as e:
        abort(400, str(e))
    # creating temporary directory for generation
    sc = sp.create_temp_directory(sd)
    # parsing nodes from directories
    nodelist = classes.Nodelist()
    pm.parse(sc, sd, nodelist)
    pm.set_connections(nodelist)
    # generating dockerfiles
    dp.generate_dockerfiles(nodelist)
    # collecting dockerfiles into a single json
    dockerfiles = sp.get_dockerfiles(nodelist)
    # deleting temporary directory
    sp.delete_temp_directory(sc)
    # collecting and returning dockerfiles as json
    return jsonify(dockerfiles)


@app.route('/docker-compose', methods=['POST'])
def docker_compose_creator():
    sd = request.get_json()
    try:
        dc.semantic_data_content_check(sd, CLIENTS_TEMPLATES_PATH, GATEWAYS_TEMPLATES_PATH,
                                       SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)
    except Exception as e:
        abort(400, str(e))
    # creating temporary directory for generation
    sc = sp.create_temp_directory(sd)
    # parsing nodes from directories
    nodelist = classes.Nodelist()
    pm.parse(sc, sd, nodelist)
    pm.set_connections(nodelist)
    # setting images for each node without creating dockerfiles for docker-compose
    sp.set_images_manually(nodelist)
    # generating docker-compose.yml
    dcp.generate_docker_compose(sc)
    dcp.generate_kafka_infrastructure(sc)
    dcp.generate_kafka_topics(sc, nodelist)
    dcp.generate_databases(sc, nodelist)
    dcp.generate_services(sc, nodelist)
    dcp.generate_gateways(sc, nodelist)
    dcp.generate_clients(sc, nodelist)
    # collecting docker-compose.yml into json
    docker_compose = sp.get_docker_compose(sc)
    # deleting temporary directory
    sp.delete_temp_directory(sc)
    # collecting and returning dockerfiles as json
    return jsonify(docker_compose)


if __name__ == "__main__":
    app.run(debug=True, port=5001, host=ALLOWED_OUTER_HOSTS)
