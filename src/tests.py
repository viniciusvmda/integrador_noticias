from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

# Create your tests here.
class AccessViewTestCase(TestCase):
	def test_access_denied(self):
		c = Client()
		response = c.get('/home/')
		self.assertEqual(403,response.status_code)

	def test_access_accepted(self):
		self.user = User.objects.create_user(username='teste',password='esw123456')
		c = Client()
		c.login(username='teste', password='esw123456')
		response = c.get('/home/')
		self.assertEqual(200,response.status_code)