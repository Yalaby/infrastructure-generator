import os
import unittest
import src.docker_compose_processor as dcp
import src.classes as classes
import shutil
import json


class DockerComposeProcessing (unittest.TestCase):
    def test_docker_compose_creation(self):
        sc = './tests/fixtures/test_creation_temp'
        os.mkdir(sc)
        dcp.generate_docker_compose(sc)
        self.assertTrue(os.path.isfile(sc + '/docker-compose.yml'))
        shutil.rmtree(sc)

    def test_kafka_infrastructure_generation(self):
        # tests that the code can generate infrastructure !! CAN FAIL IF PORTS WILL BE SWITCHED IN CONFIG FOR KAFKA!!
        # Add extracting this data from os.environ in function and in test to avoid it in future !!
        sc = './tests/fixtures/test_infa_gen_temp'
        os.mkdir(sc)
        dcp.generate_kafka_infrastructure(sc)
        with open(sc + '/docker-compose.yml', "r") as read_file:
            dc = read_file.read()
            read_file.close()
        with open('./tests/fixtures/correct/docker-compose_infrastructure.yml', "r") as read_file:
            example = read_file.read()
            read_file.close()
        self.assertEqual(dc, example)
        shutil.rmtree(sc)

    def test_kafka_topics_generation(self):
        # tests that the code can generate topics !! CAN FAIL IF PORTS FOR DATABASE_PORT_START WERE SWITCHED IN CONFIG
        # FROM 27017 !! Add extracting this data from os.environ in function and in test to avoid it in future !!
        nodelist = classes.Nodelist()
        client = classes.Client('client1', './tests/fixtures/correct/' + 'client1', 'js_react')
        nodelist.add_node(client)
        gateway = classes.Gateway('gateway_1', './tests/fixtures/correct/' + 'gateway_1', 'python')
        nodelist.add_node(gateway)
        service = classes.Service('service1', './tests/fixtures/correct/' + 'service1', 'python')
        nodelist.add_node(service)
        database = classes.Database('database1', 'mongodb')
        nodelist.add_node(database)
        client.add_connect(gateway)
        gateway.add_connect(service)
        service.add_connect(gateway)
        database.add_connect(service)
        sc = './tests/fixtures/test_topics_gen_temp'
        os.mkdir(sc)
        dcp.generate_kafka_topics(sc, nodelist)
        with open(sc + '/docker-compose.yml', "r") as read_file:
            dc = read_file.read()
            read_file.close()
        with open('./tests/fixtures/correct/docker-compose_kafka_topics.yml', "r") as read_file:
            example = read_file.read()
            read_file.close()
        self.assertEqual(dc, example)
        shutil.rmtree(sc)

    def test_databases_generation(self):
        # tests that the code can generate databases
        # Add extracting DATABASE_PORT_START data from os.environ in function and in test, after add comparison with
        # ideal example to make test more effective !!
        nodelist = classes.Nodelist()
        client = classes.Client('client1', './tests/fixtures/correct/' + 'client1', 'js_react')
        nodelist.add_node(client)
        gateway = classes.Gateway('gateway_1', './tests/fixtures/correct/' + 'gateway_1', 'python')
        nodelist.add_node(gateway)
        service = classes.Service('service1', './tests/fixtures/correct/' + 'service1', 'python')
        nodelist.add_node(service)
        database1 = classes.Database('database1', 'mongodb')
        nodelist.add_node(database1)
        database2 = classes.Database('database2', 'mongodb')
        nodelist.add_node(database2)
        client.add_connect(gateway)
        gateway.add_connect(service)
        service.add_connect(gateway)
        database1.add_connect(service)
        database2.add_connect(service)
        sc = './tests/fixtures/test_db_gen_temp'
        os.mkdir(sc)
        self.assertTrue(dcp.generate_databases(sc, nodelist))
        self.assertTrue(os.path.isdir(sc + '/database1'))
        self.assertTrue(os.path.isdir(sc + '/database2'))
        shutil.rmtree(sc)

    def test_services_generation(self):
        # tests that the code can generate services
        # Add extracting DATABASE_PORT_START and GATEWAY_PORT_START data from os.environ in function and in test, after
        # add comparison with ideal example to make test more effective !!
        nodelist = classes.Nodelist()
        client = classes.Client('client1', './tests/fixtures/correct/' + 'client1', 'js_react')
        nodelist.add_node(client)
        gateway = classes.Gateway('gateway_1', './tests/fixtures/correct/' + 'gateway_1', 'python')
        nodelist.add_node(gateway)
        service1 = classes.Service('service1', './tests/fixtures/correct/' + 'service1', 'python')
        nodelist.add_node(service1)
        service1.set_image_name(service1.name)
        service2 = classes.Service('service2', './tests/fixtures/correct/' + 'service1', 'python')
        nodelist.add_node(service2)
        service2.set_image_name(service2.name)
        database1 = classes.Database('database1', 'mongodb')
        nodelist.add_node(database1)
        database2 = classes.Database('database2', 'mongodb')
        nodelist.add_node(database2)
        client.add_connect(gateway)
        gateway.add_connect(service1)
        gateway.add_connect(service2)
        service1.add_connect(gateway)
        service2.add_connect(gateway)
        database1.add_connect(service1)
        database2.add_connect(service2)
        sc = './tests/fixtures/test_service_gen_temp'
        os.mkdir(sc)
        self.assertTrue(dcp.generate_services(sc, nodelist))
        shutil.rmtree(sc)

    def test_gateways_generation(self):
        # tests that the code can generate services
        # Add extracting GATEWAY_PORT_START data from os.environ in function and in test, after add comparison with
        # ideal example to make test more effective !!
        nodelist = classes.Nodelist()
        client = classes.Client('client1', './tests/fixtures/correct/' + 'client1', 'js_react')
        nodelist.add_node(client)
        gateway = classes.Gateway('gateway_1', './tests/fixtures/correct/' + 'gateway_1', 'python')
        nodelist.add_node(gateway)
        gateway.set_image_name(gateway.name)
        service = classes.Service('service1', './tests/fixtures/correct/' + 'service1', 'python')
        nodelist.add_node(service)
        database = classes.Database('database', 'mongodb')
        nodelist.add_node(database)
        client.add_connect(gateway)
        gateway.add_connect(service)
        service.add_connect(gateway)
        database.add_connect(service)
        sc = './tests/fixtures/test_gateways_gen_temp'
        os.mkdir(sc)
        self.assertTrue(dcp.generate_gateways(sc, nodelist))
        shutil.rmtree(sc)

    def test_clients_generation(self):
        # tests that the code can generate clients
        # Add extracting CLIENTS_PORT_START data from os.environ in function and in test, after add comparison with
        # ideal example to make test more effective !!
        nodelist = classes.Nodelist()
        client = classes.Client('client1', './tests/fixtures/correct/' + 'client1', 'js_react')
        nodelist.add_node(client)
        client.set_image_name(client.name)
        gateway = classes.Gateway('gateway_1', './tests/fixtures/correct/' + 'gateway_1', 'python')
        nodelist.add_node(gateway)
        service = classes.Service('service1', './tests/fixtures/correct/' + 'service1', 'python')
        nodelist.add_node(service)
        database = classes.Database('database', 'mongodb')
        nodelist.add_node(database)
        client.add_connect(gateway)
        gateway.add_connect(service)
        service.add_connect(gateway)
        database.add_connect(service)
        sc = './tests/fixtures/test_clients_gen_temp'
        os.mkdir(sc)
        self.assertTrue(dcp.generate_clients(sc, nodelist))
        shutil.rmtree(sc)


if __name__ == '__main__':
    unittest.main()