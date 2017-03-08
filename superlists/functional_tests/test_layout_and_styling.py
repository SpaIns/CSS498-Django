from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

#import unittest
import time
import sys
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		#Edith goes to the home page
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 768)

		#She notices the input box is nicely centered
		inputbox = self.get_item_input_box()
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=5
		)

		#She starts a new list and sees the input is nicely
		# centered there too
		inputbox.send_keys('testing')
		self.browser.find_element_by_name('email')
		inputbox = self.get_item_input_box()
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=20
		)