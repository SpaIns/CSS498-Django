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

class ItemValidationTest(FunctionalTest):
	
	
	def test_cannot_add_empty_list_items(self):
		#Edith goes to the home page and accidentally tries to submit
		# an empty list item. She hits Enter on the empty input box
		self.browser.get(self.server_url)
		self.browser.find_element_by_id('id_new_item').send_keys('\n')

		#The home page refreshes, and there is an error message saying
		# that list items cannot be blank
		error = self.browser.find_element_by_css_selector('.has_error')
		self.assertEqual(error.text, "You can't have an empty list item")

		#She tries again with some text for the item, which now works
		self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
		self.check_for_row_in_list_table('1. Buy milk')

		#Perversely, she now decides to submit a second blank list item
		self.browser.find_element_by_id('id_new_item').send_keys('\n')

		#She recieves a similar warning on the list page
		self.check_for_row_in_list_table('1: Buy milk')
		error = find_element_by_css_selector('.has_error')
		sekf,assertEqual(error.text, "You can't have an empty list item")

		#And she can correct it by filling some text in
		self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
		self.check_for_row_in_list_table('1: Buy milk')
		self.check_for_row_in_list_table('2: Make tea')

#if __name__ == '__main__':
#	unittest.main(warnings='ignore')
