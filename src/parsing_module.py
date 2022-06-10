import src.classes as classes


# parsing nodes to Client, Gateway, Service and Database class objects and adding objects to a Nodelist
def parse(sc, sd, nodelist):
    if sd["clients"]:
        for client in sd["clients"]:
            node = classes.Client(client["name"], sc + '/' + client["name"], client["language"])
            if client["connects"]:
                node.add_connect(client["connects"])
            nodelist.add_node(node)
    if sd["gateways"]:
        for gateway in sd["gateways"]:
            node = classes.Gateway(gateway["name"], sc + '/' + gateway["name"], gateway["language"])
            if gateway["connects"]:
                for connection in gateway["connects"]:
                    node.add_connect(connection)
            nodelist.add_node(node)
    if sd["services"]:
        for service in sd["services"]:
            node = classes.Service(service["name"], sc + '/' + service["name"], service["language"])
            if service["connects"]:
                for connection in service["connects"]:
                    node.add_connect(connection)
            nodelist.add_node(node)
    if sd["databases"]:
        for database in sd["databases"]:
            node = classes.Database(database["name"], database["dbtype"])
            if database["connects"]:
                for connection in database["connects"]:
                    node.add_connect(connection)
            nodelist.add_node(node)
    return True


# setting connections for each object
def set_connections(nodelist):
    for node in nodelist.nodelist:
        connections = node.connects
        node.clean_connects()
        for connection in connections:
            for n in nodelist.nodelist:
                if n.name == connection:
                    node.add_connect(n)
                    if node.node_type == 'gateway' or node.node_type == 'service':
                        n.add_connected_by(node)
    return True
