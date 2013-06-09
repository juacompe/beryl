from django.test import TestCase 

class TestHomePage(TestCase):
    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)


