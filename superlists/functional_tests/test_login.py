import re
from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

import time

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

	def test_can_get_email_link_to_login(self):
		#Edith goes to the awesome superlists site
		# and notices a "log in" section in the navbar for the first time
		# It's telling her to enter her email address, so she does

		self.browser.get(self.server_url)
		self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
		self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

		#A message appears telling her an email has been sent
		time.sleep(0.5) # I know we just got rid of almost all the hardcoded sleeps but...
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Check your email', body.text)

		#She checks her email and finds a message
		email = mail.outbox[0]
		self.assertIn(TEST_EMAIL, email.to)
		self.assertEqual(email.subject, SUBJECT)

		# It has a link to a url in it
		self.assertIn('Use this link to login', email.body)
		url_search = re.search(r'http://.+/.+$', email.body)
		if not url_search:
			self.fail(
				'could not find url in email body:\n{}'.format(email.body)
			)
		url = url_search.group(0)
		self.assertIn(self.server_url, url)

		# she clicks it
		time.sleep(10)
		self.browser.get(url)

		# she is logged in!
		self.browser.find_element_by_link_text('Log out')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(TEST_EMAIL, navbar.text)