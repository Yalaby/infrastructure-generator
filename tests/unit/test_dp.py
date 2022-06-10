import os
import unittest
import src.dockerfile_processor as dp
import src.classes as classes
import shutil


class TestDockerfileProcessing (unittest.TestCase):
    def test_dockerfile_creation(self):
        # tests that the code can successfully create dockerfiles
        os.mkdir('./tests/fixtures/test_dg')
        os.mkdir('./tests/fixtures/test_dg/client1')
        os.mkdir('./tests/fixtures/test_dg/gateway_1')
        os.mkdir('./tests/fixtures/test_dg/service1')
        nodelist = classes.Nodelist()
        client = classes.Client('client1', './tests/fixtures/test_dg/' + 'client1', 'js_react')
        nodelist.add_node(client)
        gateway = classes.Gateway('gateway_1', './tests/fixtures/test_dg/' + 'gateway_1', 'python')
        nodelist.add_node(gateway)
        service = classes.Service('service1', './tests/fixtures/test_dg/' + 'service1', 'python')
        nodelist.add_node(service)
        dp.generate_dockerfiles(nodelist)
        self.assertTrue(os.path.isfile('./tests/fixtures/test_dg/client1/dockerfile'))
        self.assertTrue(os.path.isfile('./tests/fixtures/test_dg/gateway_1/dockerfile'))
        self.assertTrue(os.path.isfile('./tests/fixtures/test_dg/service1/dockerfile'))
        shutil.rmtree('./tests/fixtures/test_dg')


if __name__ == '__main__':
    unittest.main()