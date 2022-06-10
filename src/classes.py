from config import *
import shutil


# basic class for all node types
class Node:
    def __init__(self, node_type, name):
        self.node_type = node_type  # type of the node ['client', 'gateway', 'service', 'database']
        self.name = name  # unique name of the node
        self.docker_compose_template = None  # link to a docker-compose template for the node
        self.connects = []  # other nodes to which the node is connected (one-side connection)

# basic function of adding nodes to which the node is connected (one-side connection)
    def add_connect(self, node_name):
        self.connects.append(node_name)

# basic function of cleaning list of connected nodes. Needed because while parsing we add names of nodes,
# but not objects. After parsing is done, we change names of nodes to nodes objects.
    def clean_connects(self):
        self.connects = []


# class for client nodes
class Client(Node):
    def __init__(self, name, path, language):
        Node.__init__(self, 'client', name)
        self.docker_template = CLIENTS_TEMPLATES_PATH + '/' + language  # link to a dockerfile template for the client
        self.docker_compose_template = CLIENTS_TEMPLATES_PATH + '/' + language + '_compose'
        self.path = path    # path to a source code of the client
        self.image_name = None  # docker image name of the client
        self.own_port = None    # port of client, on which it will be available from the host

# function of creating dockerfile for a client
    def create_dockerfile(self):
        shutil.copy(self.docker_template, self.path + '/dockerfile', follow_symlinks=True)

# function of setting docker image name for a client
    def set_image_name(self, image_name):
        self.image_name = image_name

# function of setting a port for a client, on which it will be available from the host
    def set_own_port(self, port):
        self.own_port = port


# class for gateway nodes
class Gateway(Node):
    def __init__(self, name, path, language):
        Node.__init__(self, 'gateway', name)
        self.docker_template = GATEWAYS_TEMPLATES_PATH + '/' + language  # link to a dockerfile template for the client
        self.docker_compose_template = GATEWAYS_TEMPLATES_PATH + '/' + language + '_compose'
        self.path = path    # path to a source code of the gateway
        self.image_name = None  # docker image name of the gateway
        self.own_port = None    # port of gateway, on which it will be available from the host
        self.connected_by = []  # services, that are connected to the gateway

# function of creating dockerfile for a gateway
    def create_dockerfile(self):
        shutil.copy(self.docker_template, self.path + '/dockerfile', follow_symlinks=True)

# function of setting docker image name for a gateway
    def set_image_name(self, image_name):
        self.image_name = image_name

# function of setting a port for a gateway, on which it will be available
    def set_own_port(self, port):
        self.own_port = port

# function of adding services, that are connected to the gateway (one-side connection)
    def add_connected_by(self, node):
        self.connected_by.append(node)


# class for service nodes
class Service(Node):
    def __init__(self, name, path, language):
        Node.__init__(self, 'service', name)
        self.docker_template = SERVICES_TEMPLATES_PATH + '/' + language  # link to a dockerfile template for the service
        self.docker_compose_template = SERVICES_TEMPLATES_PATH + '/' + language + '_compose'
        self.path = path  # path to a source code of the service
        self.image_name = None  # docker image name of the service
        self.connected_db = []  # databases, to which service is connected
        self.connected_by = []  # services/gateways, that are connected to the service (one-side connection)

# function of creating dockerfile for a service
    def create_dockerfile(self):
        shutil.copy(self.docker_template, self.path + '/dockerfile', follow_symlinks=True)

# function of setting docker image name for a service
    def set_image_name(self, image_name):
        self.image_name = image_name

# function of adding database object, to which service is connected
    def add_connected_db(self, database):
        self.connected_db.append(database)

# function of adding services/gateways, that are connected to the service (one-side connection)
    def add_connected_by(self, node):
        self.connected_by.append(node)


# class for database nodes
class Database(Node):
    def __init__(self, name, dbtype):
        Node.__init__(self, 'database', name)
        self.dbtype = dbtype
        self.own_port = None
        self.docker_compose_template = DATABASES_TEMPLATES_PATH + '/' + dbtype

# function of setting a port for a database, on which it will be available
    def set_own_port(self, port):
        self.own_port = port


# class for nodes list
class Nodelist:
    def __init__(self):
        self.nodelist = []

# function of addint node object to the list
    def add_node(self, node):
        self.nodelist.append(node)
