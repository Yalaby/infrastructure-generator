import os

from config import *
import shutil


# generating basic docker_compose.yml
def generate_docker_compose(sc):
    shutil.copy(DOCKER_COMPOSE_TEMPLATE, sc, follow_symlinks=True)
    return True


# adding infrastructure to docker-compose.yml: Zookeeper, Kafka and node, that creates topics in Kafka (Kafka-init)
def generate_kafka_infrastructure(sc):
    write_file = open(sc + '/docker-compose.yml', "a")
    with open(ZOOKEEPER_TEMPLATE, "r") as read_file:
        write_file.write(read_file.read())
        read_file.close()
    with open(KAFKA_TEMPLATE, "r") as read_file:
        write_file.write(read_file.read())
        read_file.close()
    with open(KAFKA_INIT_TEMPLATE, "r") as read_file:
        write_file.write(read_file.read())
        read_file.close()
    write_file.close()
    return True


# adding list of Kafka topics to Kafka-init that are needed according to connections between nodes
def generate_kafka_topics(sc, nodelist):
    with open(KAFKA_TOPIC_TEMPLATE, "r") as read_file:
        data = read_file.read()
        read_file.close()
    write_file = open(sc + '/docker-compose.yml', "a")
    for node in nodelist.nodelist:
        if node.node_type == 'service' or node.node_type == 'gateway':
            for connection in node.connects:
                kafka_topic = data.replace('{TOPIC_NAME}', node.name.replace('_', '-') + '-' +
                                           connection.name.replace('_', '-') + '-topic')
                write_file.write('\n' + kafka_topic)
    write_file.write('"\n\n')
    write_file.close()
    return True


# adding databases to docker-compose.yml
def generate_databases(sc, nodelist):
    write_file = open(sc + '/docker-compose.yml', "a")
    port_counter = DATABASE_PORT_START
    for node in nodelist.nodelist:
        if node.node_type == 'database':
            with open(node.docker_compose_template, "r") as read_file:
                data = read_file.read()
                read_file.close()
            if not os.path.isdir(sc + '/' + node.name):
                os.mkdir(sc + '/' + node.name)
            database_node = data.replace('{DOCKERBRIDGE_PORT}', str(port_counter))
            database_node = database_node.replace('{EXPOSED_PORT}', str(port_counter))
            database_node = database_node.replace('{STORAGE_PATH}', sc + '/' + node.name)
            database_node = database_node.replace('{NODE_NAME}', node.name)
            database_node = database_node.replace('{DB_NAME}', node.name)
            write_file.write(database_node + '\n')
            node.set_own_port(port_counter)
            for connection in node.connects:
                connection.add_connected_db(node)
            port_counter += 1
    write_file.close()
    return True


# adding services to docker-compose.yml
def generate_services(sc, nodelist):
    write_file = open(sc + '/docker-compose.yml', "a")
    for node in nodelist.nodelist:
        if node.node_type == 'service':
            with open(node.docker_compose_template, "r") as read_file:
                data = read_file.read()
                read_file.close()
            service_node = data.replace('{IMAGE_NAME}', node.image_name)
            service_node = service_node.replace('{NODE_NAME}', node.name)
            if node.connects or node.connected_db:
                service_node += '    depends_on:'
                if node.connects:
                    service_node += '\n      - kafka'
                if node.connected_db:
                    for db in node.connected_db:
                        service_node += '\n      - ' + db.name
                service_node += '\n    environment:\n'
                if node.connects or node.connected_by:
                    with open(KAFKA_ENVIRONMENT_TEMPLATE, "r") as read_file:
                        data = read_file.read()
                        read_file.close()
                    service_node += data
                    for connection in node.connects:
                        service_node += '      ' + node.name.upper() + '_' + connection.name.upper() + '_TOPIC' + \
                                        ': ' + node.name.replace('_', '-') + '-' + connection.name.replace('_', '-') + \
                                        '-topic\n'
                    for connection in node.connected_by:
                        service_node += '      ' + connection.name.upper() + '_' + node.name.upper() + '_TOPIC' + \
                                        ': ' + connection.name.replace('_', '-') + '-' + node.name.replace('_', '-') + \
                                        '-topic\n'
                if node.connected_db:
                    for db in node.connected_db:
                        with open(DATABASES_TEMPLATES_PATH + '/' + db.dbtype + '_environment', "r") as read_file:
                            data = read_file.read()
                            read_file.close()
                        service_node += data.replace('{DB_TYPE}', db.dbtype)
                        service_node = service_node.replace('{DB_HOST}', db.name)
                        service_node = service_node.replace('{DB_PORT}', str(db.own_port))
                        service_node = service_node.replace('{DB_NAME}', db.name)
                        service_node = service_node.replace('{DB_COLLECTION}', db.name)
            write_file.write(service_node + '\n')
    write_file.close()
    return True


# adding gateways to docker-compose.yml
def generate_gateways(sc, nodelist):
    write_file = open(sc + '/docker-compose.yml', "a")
    port_counter = GATEWAY_PORT_START
    for node in nodelist.nodelist:
        if node.node_type == 'gateway':
            with open(node.docker_compose_template, "r") as read_file:
                data = read_file.read()
                read_file.close()
            gateway_node = data.replace('{IMAGE_NAME}', node.image_name)
            gateway_node = gateway_node.replace('{NODE_NAME}', node.name)
            gateway_node = gateway_node.replace('{DOCKERBRIDGE_PORT}', str(port_counter))
            gateway_node = gateway_node.replace('{EXPOSED_PORT}', str(port_counter))
            if node.connects or node.connected_by:
                gateway_node += '    depends_on:'
                gateway_node += '\n      - kafka'
                gateway_node += '\n    environment:\n'
                with open(KAFKA_ENVIRONMENT_TEMPLATE, "r") as read_file:
                    data = read_file.read()
                    read_file.close()
                gateway_node += data
                for connection in node.connects:
                    gateway_node += '      ' + node.name.upper() + '_' + connection.name.upper() + '_TOPIC' + \
                                    ': ' + node.name.replace('_', '-') + '-' + connection.name.replace('_', '-') + \
                                    '-topic\n'
                gateway_node += '      ALLOWED_OUTER_HOSTS: 0.0.0.0\n'
                for connection in node.connected_by:
                    gateway_node += '      ' + connection.name.upper() + '_' + node.name.upper() + '_TOPIC' + \
                                    ': ' + connection.name.replace('_', '-') + '-' + node.name.replace('_', '-') + \
                                    '-topic\n'
            node.set_own_port(port_counter)
            port_counter += 1
            write_file.write(gateway_node + '\n')
    write_file.close()
    return True


# adding clients to docker-compose.yml
def generate_clients(sc, nodelist):
    write_file = open(sc + '/docker-compose.yml', "a")
    port_counter = CLIENTS_PORT_START
    for node in nodelist.nodelist:
        if node.node_type == 'client':
            with open(node.docker_compose_template, "r") as read_file:
                data = read_file.read()
                read_file.close()
            client_node = data.replace('{NODE_NAME}', node.name)
            client_node = client_node.replace('{IMAGE_NAME}', node.image_name)
            client_node = client_node.replace('{DOCKERBRIDGE_PORT}', str(port_counter))
            client_node = client_node.replace('{EXPOSED_PORT}', str(port_counter))
            if node.connects:
                client_node = client_node.replace('{GATEWAY_PORT}', str(node.connects[0].own_port))
            write_file.write(client_node + '\n')
            port_counter += 1
    write_file.close()
    return True


# running docker-compose.yml
def run_docker_compose(sc):
    os.system('cd ' + sc + '; docker-compose up -d')
