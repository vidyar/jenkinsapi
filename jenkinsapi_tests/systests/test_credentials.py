'''
System tests for `jenkinsapi.jenkins` module.
'''
import logging
import unittest
from jenkinsapi.credential import Credential
from jenkinsapi_tests.systests.base import BaseSystemTest
from jenkinsapi_tests.test_utils.random_strings import random_string

log = logging.getLogger(__name__)


class TestNodes(BaseSystemTest):

    TEST_NODE_NAME = 'test_node_jenkinsapi'

    def tearDown(self):
        super(TestNodes, self).tearDown()

    def test_create_credential(self):
        name = random_string()
        c = self.jenkins.create_credential(name, password=random_string())
        self.assertIsInstance(c, Credential)


if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
