from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token
import logging
#from unittest.mock import patch, call

User = get_user_model()

#@patch('accounts.authentication.requests.post')
class AuthenticateTest(TestCase):

	def test_returns_None_if_no_such_token(self):
		result = PasswordlessAuthenticationBackend().authenticate(
			'no-such-token'
		)
		self.assertIsNone(result)

	def test_returns_new_user_with_correct_email_if_token_exists(self):
		email = 'edith@example.com'
		token = Token.objects.create(email=email)
		user = PasswordlessAuthenticationBackend().authenticate(token.uid)
		new_user = User.objects.get(email=email)
		self.assertEqual(user, new_user)

	def test_returns_existing_user_with_correct_email_if_token_exists(self):
		email = 'edith@example.com'
		existing_user = User.objects.create(email=email)
		token = Token.objects.create(email=email)
		user = PasswordlessAuthenticationBackend().authenticate(token.uid)
		self.assertEqual(user, existing_user)

	#def test_logs_non_okay_responses_from_persona(self, mock_post):
	#	response_json = {
	#		'status': 'not okay', 'reason': 'eg, audience mismatch'
	#	}
	#	mock_post.return_value.ok = True
	#	mock_post.return_value.json.return_value = response_json

	#	logger = logging.getLogger('accounts.authentication')
	#	with patch.object(logger, 'warning') as mock_log_warning:
	#		self.backend.authenticate('an assertion')

	#	mock_log_warning.assert_called_once_with(
	#		'Persona says no. Json was: {}'.format(response_json)
	#	)

class GetUserTest(TestCase):

	def test_gets_user_by_email(self):
		User.objects.create(email='another@example.com')
		desired_user = User.objects.create(email='edith@example.com')
		found_user = PasswordlessAuthenticationBackend().get_user(
			'edith@example.com'
		)
		self.assertEqual(found_user, desired_user)

	def test_returns_None_if_no_user_with_that_email(self):
		self.assertIsNone(
			PasswordlessAuthenticationBackend().get_user('edith@example.com')
		)