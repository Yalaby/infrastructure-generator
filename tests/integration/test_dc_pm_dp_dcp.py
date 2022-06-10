import shutil
import unittest
import src.parsing_module as pm
import src.dockerfile_processor as dp
import src.directory_check as dc
import src.docker_compose_processor as dcp
import src.classes as classes
from config import *
import json
import os


class TestCreationComplex (unittest.TestCase):
    def test_dockerfiles_and_compose_creaction(self):
        #  tests that the code can correctly check directories, create dockerfiles and correct docker-compose file. May
        #  fail if not using default config values (same as for test_dcp in ../unit)
        sc = './tests/fixtures/temp_dockerfiles_and_compose_creation'
        if os.path.isdir(sc):
            shutil.rmtree(sc)
        shutil.copytree('./tests/fixtures/clear_input_data', sc)
        sd = sc
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

        # generating docker-compose.yml
        dcp.generate_docker_compose(sc)
        dcp.generate_kafka_infrastructure(sc)
        dcp.generate_kafka_topics(sc, nodelist)
        dcp.generate_databases(sc, nodelist)
        dcp.generate_services(sc, nodelist)
        dcp.generate_gateways(sc, nodelist)
        dcp.generate_clients(sc, nodelist)

        created = open(sc + "/docker-compose.yml", "r")
        example = open("./tests/fixtures/correct/docker-compose.yml", "r+")
        l_created = created.readlines()
        l_example = example.readlines()
        self.maxDiff = None
        self.assertEqual(len(l_example), len(l_created))
        for i in range(len(l_example)):
            # deletes lines where path for data storage set because test would fail on different machines otherwise
            if ':/data/db' not in l_example[i]:
                self.assertEqual(l_example[i], l_created[i])
        created.close()
        example.close()

        self.assertTrue(os.path.isfile(sc + '/gateway_1/dockerfile'))
        self.assertTrue(os.path.isfile(sc + '/marketplace_admin/dockerfile'))
        self.assertTrue(os.path.isfile(sc + '/payment/dockerfile'))
        self.assertTrue(os.path.isfile(sc + '/user_interface/dockerfile'))
        self.assertTrue(os.path.isfile(sc + '/warehouse/dockerfile'))
        self.assertTrue(os.path.isdir(sc + '/database1'))

        shutil.rmtree(sc)
