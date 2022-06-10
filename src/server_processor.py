# auxiliary functions for server
import random
import string
import os
import shutil


# creating temporary source code directory for generators
def create_temp_directory(sd):
    sc = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    if not os.path.isdir(sc):
        os.mkdir(sc)
    if sd["clients"]:
        for client in sd["clients"]:
            os.mkdir(sc + '/' + client["name"])
    if sd["gateways"]:
        for gateway in sd["gateways"]:
            os.mkdir(sc + '/' + gateway["name"])
    if sd["services"]:
        for service in sd["services"]:
            os.mkdir(sc + '/' + service["name"])
    return sc


def delete_temp_directory(sc):
    shutil.rmtree(sc)
    return True


def get_dockerfiles(nodelist):
    json = []
    for node in nodelist.nodelist:
        if node.node_type != 'database':
            with open(node.path + '/dockerfile', "r") as read_file:
                json.append({'name': node.name, "dockerfile": read_file.read()})
                read_file.close()
    return json


def set_images_manually(nodelist):
    for node in nodelist.nodelist:
        if node.node_type != 'database':
            node.set_image_name(node.name + ':latest')


def get_docker_compose(sc):
    json = {}
    with open(sc + '/docker-compose.yml', "r") as read_file:
        json["docker-compose"] = read_file.read()
        read_file.close()
    return json
