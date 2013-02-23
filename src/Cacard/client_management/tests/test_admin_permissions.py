'''
Created on Feb 20, 2013

@author: oleg
'''
from unittest import TestCase
from BeautifulSoup import BeautifulSoup
from django.contrib.auth.models import User
from django.test.client import Client

class UserTest(TestCase):
    user = 'fakeuser'
    password = 'fakepass'
    user_is_staff = True
    def setUp(self):
        self.client = Client()
        self.user, _ = User.objects.get_or_create(username=self.user)
        self.user.is_staff = self.user_is_staff
        self.user.set_password(self.password)
        self.user.save()
        self.client.login(username=self.user, password=self.password)

    def check_presence(self, data, tag, find_all=[], find_any=[]):
        soup = BeautifulSoup(data)
        if find_all:
            self.assertTrue(all([any([find in t.text for t in soup(tag)])
                                             for find in find_all]))
        if find_any:
            self.assertTrue(any([any([find in t.text for t in soup(tag)])
                                             for find in find_any]))


class TestOpenSomething(UserTest):
    def setUp(self):
        super(TestOpenSomething, self).setUp()
        self.user

    def test(self):
        res = self.client.get('/admin/calling_card/brand/')
#        import ipdb; ipdb.set_trace()
        self.assertEqual(res.status_code, 200)
        self.check_presence(res.content, 'title',
                            find_all=['Select brand to change'])


class TestCantOpenSomething(UserTest):
    def test(self):
        res = self.client.get('/admin/calling_card/brand/')
        self.assertEqual(res.status_code, 403)
        self.check_presence(res.content, 'h1',
                            find_all=['Forbidden'])


class TestNotStuff(UserTest):
    user_is_staff = False
    def test_unauthorized(self):
        res = self.client.get('/admin/calling_card/brand/')
        self.assertEqual(res.status_code, 200)
        self.check_presence(res.content, 'title',
                            find_all=['Log in'])