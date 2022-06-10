import unittest
import src.parsing_module as pm
import src.classes as classes
import json


class TestParse (unittest.TestCase):
    def test_parsing(self):
        #  tests that the code can successfully parse correct data
        sc = './tests/fixtures/correct'
        with open('./tests/fixtures/correct/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        nodelist = classes.Nodelist()
        self.assertTrue(pm.parse(sc, sd, nodelist))

    def test_set_connections(self):
        # tests that the code can successfully set connections between nodes
        nodelist = classes.Nodelist()
        client = classes.Client('client1', './tests/fixtures/correct/' + 'client1', 'js_react')
        client.add_connect('gateway_1')
        nodelist.add_node(client)
        gateway = classes.Gateway('gateway_1', './tests/fixtures/correct/' + 'gateway_1', 'python')
        gateway.add_connect('service1')
        nodelist.add_node(gateway)
        service = classes.Service('service1', './tests/fixtures/correct/' + 'service1', 'python')
        service.add_connect('gateway_1')
        nodelist.add_node(service)
        database = classes.Database('database1', 'mongodb')
        database.add_connect('service1')
        nodelist.add_node(database)
        self.assertTrue(pm.set_connections(nodelist))

    def test_set_connections_objects(self):
        # tests that the code can successfully set connections between nodes as objects
        nodelist = classes.Nodelist()
        client = classes.Client('client1', './tests/fixtures/correct/' + 'client1', 'js_react')
        client.add_connect('gateway_1')
        nodelist.add_node(client)
        gateway = classes.Gateway('gateway_1', './tests/fixtures/correct/' + 'gateway_1', 'python')
        gateway.add_connect('service1')
        nodelist.add_node(gateway)
        service = classes.Service('service1', './tests/fixtures/correct/' + 'service1', 'python')
        service.add_connect('gateway_1')
        nodelist.add_node(service)
        database = classes.Database('database1', 'mongodb')
        database.add_connect('service1')
        nodelist.add_node(database)
        pm.set_connections(nodelist)
        self.assertIs(type(nodelist.nodelist[1].connects[0]), classes.Service)


if __name__ == '__main__':
    unittest.main()
