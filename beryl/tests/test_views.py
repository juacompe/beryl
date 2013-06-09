from django.test import TestCase 
from testutils import factory

class TestHomePage(TestCase):
    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_login(self):
        factory.create_superuser()
        post_data = {'username': 'admin', 'password': 'iamnottellingyou'}
        response = self.client.post('/accounts/login/', post_data, follow=True)
        self.assert_that_is_logged_in(self.client.session)
        self.assert_that_can_see_logout_button(response)

    def assert_that_is_logged_in(self, session):
        self.assertIn('_auth_user_id', session)

    def assert_that_can_see_logout_button(self, response):
        self.assertContains(response, 'logout')
        
    def test_logout(self):
        self.test_login()
        response = self.client.get('/accounts/logout/')
        self.assertNotIn('_auth_user_id', self.client.session)
        
