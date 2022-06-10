import argparse
from config import *
import src.classes as classes
import src.parsing_module as pm
import src.directory_check as dc
import src.dockerfile_processor as dp
import src.docker_compose_processor as dcp
import json


# parsing arguments
parser = argparse.ArgumentParser(description='Arguments for infrastructure generator:')
parser.add_argument("-sc", default='~/', help="Path to a source code")
parser.add_argument("-sd", default='~/', help="Path to semantic data")
parser.add_argument("-ci", action='store_const', const=True, help="If setted, creates images")
parser.add_argument("-run", action='store_const', const=True, help="If setted, creates images and runs docker-compose")
args = parser.parse_args()
sc = args.sc
sd = args.sd
ci = args.ci
run = args.run


# checking directories from arguments
sd = dc.semantic_data_check(sd)
with open(sd, "r") as read_file:
    sd = json.load(read_file)
    read_file.close()
dc.semantic_data_content_check(sd, CLIENTS_TEMPLATES_PATH, GATEWAYS_TEMPLATES_PATH, SERVICES_TEMPLATES_PATH,
                               DATABASES_TEMPLATES_PATH)
sc = dc.source_code_check(sc)
dc.source_code_content_check(sc, sd)

# parsing nodes from directories
nodelist = classes.Nodelist()
pm.parse(sc, sd, nodelist)
pm.set_connections(nodelist)

# generating dockerfiles
dp.generate_dockerfiles(nodelist)

# creating docker images if required
if ci or run:
    dp.generate_images(nodelist)

# generating docker-compose.yml
dcp.generate_docker_compose(sc)
dcp.generate_kafka_infrastructure(sc)
dcp.generate_kafka_topics(sc, nodelist)
dcp.generate_databases(sc, nodelist)
dcp.generate_services(sc, nodelist)
dcp.generate_gateways(sc, nodelist)
dcp.generate_clients(sc, nodelist)

# running docker-compose if required
if run:
    dcp.run_docker_compose(sc)
