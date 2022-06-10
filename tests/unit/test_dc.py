import unittest
import src.directory_check as dc
from config import *
import json


class TestPath (unittest.TestCase):
    def test_right_without_end(self):
        # test that the code can check a right path without /sematic_data.json in the end
        path = './tests/fixtures/correct'
        self.assertEqual(dc.semantic_data_check(path), './tests/fixtures/correct/semantic_data.json')

    def test_right_with_end(self):
        # test that the code can check a right path with /sematic_data.json in the end
        path = './tests/fixtures/correct/semantic_data.json'
        self.assertEqual(dc.semantic_data_check(path), './tests/fixtures/correct/semantic_data.json')

    def test_right_with_slash(self):
        # test that the code can check a right path with / in the end
        path = './tests/fixtures/correct/'
        self.assertEqual(dc.semantic_data_check(path), './tests/fixtures/correct/semantic_data.json')

    def test_wrong_path(self):
        # test that the code can detect a wrong path
        path = './tests/'
        self.assertRaises(FileNotFoundError, dc.semantic_data_check, path)

    def test_wrong_filename(self):
        # test that the code can detect a wrong path
        path = './tests/app.py'
        self.assertRaises(NameError, dc.semantic_data_check, path)

    def test_wrong_sourcecode_dir(self):
        # test that the code can detect a wrong sourcecode path
        path = './tests/qwerty'
        self.assertRaises(NotADirectoryError, dc.source_code_check, path)

    def test_right_sourcecode_dir(self):
        # test that the code can detect a right sourcecode path
        path = './tests/fixtures/correct'
        s = dc.source_code_check(path)
        self.assertTrue(s.endswith(path[1:]))

    def test_right_sourcecode_dir_slash(self):
        # test that the code can delete / in the end of sourcecode path
        path = './tests/fixtures/correct/'
        s = dc.source_code_check(path)
        self.assertTrue(s.endswith(path[1:24]))


class TestContent (unittest.TestCase):
    def test_correct_semantic_data(self):
        # test that the code can detect correct semantic_data.json
        with open('./tests/fixtures/correct/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertTrue(dc.semantic_data_content_check(sd, CLIENTS_TEMPLATES_PATH, GATEWAYS_TEMPLATES_PATH,
                                                       SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH))

    def test_semantic_data_without_name(self):
        # test that the code can detect correct semantic_data.json
        with open('./tests/fixtures/no_name/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertRaises(ValueError, dc.semantic_data_content_check, sd, CLIENTS_TEMPLATES_PATH,
                          GATEWAYS_TEMPLATES_PATH, SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)

    def test_semantic_data_without_name(self):
        # test that the code can detect nodes without names in semantic_data.json
        with open('./tests/fixtures/no_name/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertRaises(ValueError, dc.semantic_data_content_check, sd, CLIENTS_TEMPLATES_PATH,
                          GATEWAYS_TEMPLATES_PATH, SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)

    def test_semantic_data_without_language(self):
        # test that the code can detect nodes without names in semantic_data.json
        with open('./tests/fixtures/no_language/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertRaises(ValueError, dc.semantic_data_content_check, sd, CLIENTS_TEMPLATES_PATH,
                          GATEWAYS_TEMPLATES_PATH, SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)

    def test_semantic_data_with_incorrect_language(self):
        # test that the code can detect nodes with incorrect language in semantic_data.json
        with open('./tests/fixtures/incorrect_language_and_dir_content/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertRaises(ValueError, dc.semantic_data_content_check, sd, CLIENTS_TEMPLATES_PATH,
                          GATEWAYS_TEMPLATES_PATH, SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)

    def test_semantic_data_lot_connections_client(self):
        # tests that the code can detect clients with more that one connection
        with open('./tests/fixtures/lot_connections_client/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertRaises(ValueError, dc.semantic_data_content_check, sd, CLIENTS_TEMPLATES_PATH,
                          GATEWAYS_TEMPLATES_PATH, SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)

    def test_semantic_data_wrong_connections_client(self):
        # tests that the code can detect clients with that connect not to gateway
        with open('./tests/fixtures/wrong_connections_client/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertRaises(ValueError, dc.semantic_data_content_check, sd, CLIENTS_TEMPLATES_PATH,
                          GATEWAYS_TEMPLATES_PATH, SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)

    def test_semantic_data_wrong_connections_gateway(self):
        # tests that the code can detect gateways that connect not to gateway or service
        with open('./tests/fixtures/wrong_connections_gateway/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertRaises(ValueError, dc.semantic_data_content_check, sd, CLIENTS_TEMPLATES_PATH,
                          GATEWAYS_TEMPLATES_PATH, SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)

    def test_semantic_data_wrong_connections_service(self):
        # tests that the code can detect services that connect not to gateway or service
        with open('./tests/fixtures/wrong_connections_service/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertRaises(ValueError, dc.semantic_data_content_check, sd, CLIENTS_TEMPLATES_PATH,
                          GATEWAYS_TEMPLATES_PATH, SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)

    def test_semantic_data_wrong_connections_database(self):
        # tests that the code can detect services that connect not to gateway or service
        with open('./tests/fixtures/wrong_connections_service/semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertRaises(ValueError, dc.semantic_data_content_check, sd, CLIENTS_TEMPLATES_PATH,
                          GATEWAYS_TEMPLATES_PATH, SERVICES_TEMPLATES_PATH, DATABASES_TEMPLATES_PATH)

    def test_sourcecode_content_correct(self):
        # tests that the code can detect correct sourcecode directory content
        sc = './tests/fixtures/correct/'
        with open(sc + 'semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertTrue(dc.source_code_content_check(sc, sd))

    def test_sourcecode_content_incorrect(self):
        # tests that the code can detect incorrect sourcecode directory content
        sc = './tests/fixtures/incorrect_language_and_dir_content/'
        with open(sc + 'semantic_data.json', "r") as read_file:
            sd = json.load(read_file)
            read_file.close()
        self.assertRaises(NotADirectoryError, dc.source_code_content_check, sc, sd)


if __name__ == '__main__':
    unittest.main()
