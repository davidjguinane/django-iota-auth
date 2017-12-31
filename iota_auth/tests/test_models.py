from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(TestCase):

	# Test that User is created
	def setUp(self, password):
		User.objects.create(email='test@email.com', password='TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESHERE9TESTSEEDGOESH')

	# Test user exists
	def test_user_exists(self):
		user = User.objects.get(email='test@email.com')

	# Test that password validator rejects invalid seed
	def check_invalid_password(self):
		pass

	# Test that password validator accepts valid seed
	def check_valid_password(self):
		pass

	# Test that email validator checks for unique email
	def check_valid_email(self):
		pass