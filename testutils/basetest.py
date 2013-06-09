from django.test import TestCase
from testutils import factory

class AdminTestCase(TestCase):
    def login_as_admin(self):
        factory.create_superuser('admin', '1234')
        self.client.login(username='admin', password='1234')
        
