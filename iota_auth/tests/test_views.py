from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

class IotaAuthViewTests(TestCase):

	@classmethod
	def setUpClass(self):
		self.client = Client()
		User.objects.create(email='test@email.com', password='TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESH')

	def test_user_login(self):
		self.client.login(email='test@email.com', password='TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESH')
		response = self.client.get('/account/1/')
		self.assertEqual(response.status_code, 200)
		self.client.logout()
		response = self.client.get('/account/1/')
		self.assertRedirect(response, '/login/')

	# Test the login view for GET request
	def test_get_login_view(self):
		response = self.client.get('/login/')
		self.assertEqual(response.status_code, 200)

	# Test the login view for POST request
	def test_post_login_view(self):
		response = self.client.post('/login/', {'email': 'test@email.com', 'password': 'TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESH'})
		self.assertEqual(response.status_code, 200)

	# Test the signup view for GET request
	def test_get_signup_view(self):
		response = self.client.get('/signup/')
		self.assertEqual(response.status_code, 200)

	# Test the signup view for GET request
	def test_post_signup_view(self):
		response = self.client.post('/signup/', {'first_name': 'Bob','last_name': 'Dylan','email': 'bobbyd@email.com', 'password': 'TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESH'})
		self.assertEqual(response.status_code, 200)