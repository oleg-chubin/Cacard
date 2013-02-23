'''
Created on Feb 22, 2013

@author: oleg
'''
from unittest import TestCase

from Cacard.client_management import utils

class TestCreateClientInfrastructure(TestCase):
    def test_call(self):
        utils.create_client_infrastructure()