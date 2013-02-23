'''
Created on Feb 22, 2013

@author: oleg
'''
from unittest import TestCase
from django.contrib.auth.models import User, Group, Permission

from Cacard.client_management import utils

class TestCreateClientInfrastructure(TestCase):
    client_name = 'some_client'
    def test_call(self):
        utils.create_client_infrastructure(self.client_name)
        self.assertTrue(User.objects.filter(username=self.client_name).exists())
        self.assertTrue(Group.objects.filter(name=self.client_name).exists())
        group = Group.objects.get(name=self.client_name)
        user = User.objects.get(username=self.client_name)
        self.assertTrue(user.groups.filter(name=self.client_name).exists())
