from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException

from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

#import unittest
import time
import sys
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url


	def setUp(self):
		binary = FirefoxBinary(r'/home/spa/firefox/firefox') 
		self.browser = webdriver.Firefox(firefox_binary=binary)
		#self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.refresh()
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except(AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def wait_for_error_element(self):
		start_time = time.time()
		while True:
			try:
				element = self.browser.find_element_by_css_selector('.has-error')
				return element
			except(NoSuchElementException, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')