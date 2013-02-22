'''
Created on Feb 20, 2013

@author: oleg
'''
from unittest import TestCase
from BeautifulSoup import BeautifulSoup
from django.contrib.auth.models import User
from django.test.client import Client

class TestOpenSomething(TestCase):
    def setUp(self):
        self.client = Client()
        self.user, _ = User.objects.get_or_create(username='fakename')#'fake@pukkared.com'
        self.user.is_superuser=True
        self.user.set_password('mypassword')
        self.user.save()

        #use test client to perform login

    def check_presence(self, data, tag, find_all=[], find_any=[]):
        soup = BeautifulSoup(data)
        if find_all:
            self.assertTrue(all([any([content in t.text for t in soup(tag)])
                                             for content in find_all]))
        if find_any:
            self.assertTrue(any([any([content in t.text for t in soup(tag)])
                                             for content in find_any]))

    def test(self):
        self.user.is_superuser = self.user.is_staff = True
        self.user.save()
        user = self.client.login(username='fakename',
                                 password='mypassword')
        res = self.client.get('/admin/calling_card/brand/')
        self.assertEqual(res.status_code, 200)
        self.check_presence(res.content, 'title',
                            find_all=['Select brand to change'])

    def test_unauthorized(self):
        self.user.is_superuser = self.user.is_staff = False
        self.user.save()
        res = self.client.get('/admin/calling_card/brand/')
        self.check_presence(res.content, 'title',
                            find_all=['Log in'])