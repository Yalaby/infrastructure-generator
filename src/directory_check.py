import os


# checking if semantic_data.json file exists
def semantic_data_check(sd):
    if sd[-1] == '/':
        sd = sd[:-1]
    if os.path.isdir(sd):
        if not os.path.isfile(sd + '/semantic_data.json'):
            raise FileNotFoundError('semantic_data.json does not exists in path ' + sd)
        else:
            return sd + '/semantic_data.json'
    elif sd.endswith('semantic_data.json'):
        return sd
    else:
        raise NameError('incorrect semantic_data.json file name')


# checking content of semantic_data.json
def semantic_data_content_check(sd, clients_templates_path, gateways_templates_path, services_templates_path,
                                databases_templates_path):
    clients_names = []
    gateways_names = []
    services_names = []
    databases_names = []
    # checking if clients section in semantic_data.json is correct
    if "clients" in sd and sd["clients"]:
        for client in sd["clients"]:
            if "name" not in client or not client["name"]:
                raise ValueError('no name for at least one of clients in semantic_data.json!')
            for cli in sd["clients"]:
                clients_names.append(cli["name"])
            if "language" not in client or not client["language"]:
                raise ValueError('language for clients "' + client["name"] + '" is not stated in semantic_data.json!')
            if not os.path.isfile(clients_templates_path + '/' + client["language"]):
                raise ValueError('unsupported language "' + client["language"] + '" for client "' +
                                 client["name"] + '"')
    # checking if gateways section in semantic_data.json is correct
    if "gateways" in sd and sd["gateways"]:
        for gateway in sd["gateways"]:
            if "name" not in gateway or not gateway["name"]:
                raise ValueError('no name for at least one of gateways in semantic_data.json!')
            for gway in sd["gateways"]:
                gateways_names.append(gway["name"])
            if "language" not in gateway or not gateway["language"]:
                raise ValueError('language for gateway "' + gateway["name"] + '" is not stated!')
            if not os.path.isfile(gateways_templates_path + '/' + gateway["language"]):
                raise ValueError('unsupported language "' + gateway["language"] + '" for gateway "' +
                                 gateway["name"] + '"')
    # checking if services section in semantic_data.json is correct
    if "services" in sd and sd["services"]:
        for service in sd["services"]:
            if "name" not in service or not service["name"]:
                raise ValueError('no name for at least one of services in semantic_data.json!')
            for serv in sd["services"]:
                services_names.append(serv["name"])
            if "language" not in service or not service["language"]:
                raise ValueError('language for service "' + service["name"] + '" is not stated!')
            if not os.path.isfile(services_templates_path + '/' + service["language"]):
                raise ValueError('unsupported language "' + service["language"] + '" for service "' +
                                 service["name"] + '"')
    # checking if databases section in semantic_data.json is correct
    if "databases" in sd and sd["databases"]:
        for database in sd["databases"]:
            if "name" not in database or not database["name"]:
                raise ValueError('no name for at least one of databases in semantic_data.json!')
            for db in sd["databases"]:
                databases_names.append(db["name"])
            if "dbtype" not in database or not database["dbtype"]:
                raise ValueError('no dbtype for database "' + database['name'] + '" in semantic_data.json!')
            if not os.path.isfile(databases_templates_path + '/' + database["dbtype"]):
                raise ValueError('unsupported database dbtype "' + database["dbtype"] + '" for database "' +
                                 database['name'] + '"')
    # checking if connections of clients in semantic_data.json are correct
    if "clients" in sd and sd["clients"]:
        for client in sd["clients"]:
            if "connects" in client:
                if client["connects"]:
                    if type(client["connects"]) != str:
                        raise ValueError('"connects" field must be string with 1 connection! in client "' +
                                         client["name"] + '"')
                if client["connects"] not in gateways_names:
                    raise ValueError('wrong connection "' + client["connects"] + '" in service "' + client["name"] + '"'
                                     )
    # checking if connections of gateways in semantic_data.json are correct
    if "gateways" in sd and sd["gateways"]:
        for gateway in sd["gateways"]:
            if "connects" in gateway and gateway["connects"]:
                if gateway["name"] in gateway["connects"]:
                    raise ValueError('gateway cannot connect itself! in gateway "' + gateway["name"] + '"')
                for connection in gateway["connects"]:
                    if connection not in gateways_names and connection not in services_names:
                        raise ValueError('unknown connection "' + connection + '" in gateway "' + gateway["name"] + '"')
    # checking if connections of services in semantic_data.json are correct
    if "services" in sd and sd["services"]:
        for service in sd["services"]:
            if "connects" in service and service["connects"]:
                if service["name"] in service["connects"]:
                    raise ValueError('service cannot connect itself! in service "' + service["name"] + '"')
                for connection in service["connects"]:
                    if connection not in services_names and connection not in gateways_names:
                        raise ValueError('unknown connection "' + connection + '" in service "' + service["name"] + '"')
    # checking if connections of databases in semantic_data.json are correct
    if "databases" in sd and sd["databases"]:
        for database in sd["databases"]:
            if "connects" in database and database["connects"]:
                for connection in database["connects"]:
                    if connection in clients_names:
                        raise ValueError('database cannot be connected to clients! in database "'
                                         + database["name"] + '"')
                    if connection in gateways_names:
                        raise ValueError('database cannot be connected to gateways! in database "'
                                         + database["name"] + '"')
                    if connection not in services_names:
                        raise ValueError('unknown connection "' + connection + '" in database "' + database["name"] +
                                         '"')
    return True


# checking if source code directory exists
def source_code_check(sc):
    if sc[-1] == '/':
        sc = sc[:-1]
    if not os.path.isdir(sc):
        raise NotADirectoryError('source code directory does not exist!')
    sc = os.path.abspath(sc)
    return sc


# checking if source code directory contains source code for each node
def source_code_content_check(sc, sd):
    for client in sd["clients"]:
        if not os.path.isdir(sc + '/' + client["name"] + '/src'):
            raise NotADirectoryError('source code directory for client "' + client["name"] + '" does not exist!')
    for gateway in sd["gateways"]:
        if not os.path.isdir(sc + '/' + gateway["name"] + '/src'):
            raise NotADirectoryError('source code directory for gateway "' + gateway["name"] + '" does not exist!')
    for service in sd["services"]:
        if not os.path.isdir(sc + '/' + service["name"] + '/src'):
            raise NotADirectoryError('source code directory for service "' + service["name"] + '" does not exist!')
    return True
