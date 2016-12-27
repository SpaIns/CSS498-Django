from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase

#import unittest
import time
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		#caps = DesiredCapabilities.FIREFOX
		#caps["marionette"] = True
		#caps["binary"] = 'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
		binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe') 
		#browser = webdriver.Firefox(capabilities=caps)
		self.browser = webdriver.Firefox(firefox_binary=binary)
		self.browser.implicitly_wait(3)
		#browser = webdriver.Chrome()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrive_it_later(self):
		#Edith has heard about a cool new online to-do app. She goes
		#to check out it's homepage...
		self.browser.get(self.live_server_url)

		#she notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		#she is invited to enter a to-do item straight away

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		#She types "buy peacock feather" into a text box

		inputbox.send_keys('Buy peacock feathers')

		#When she hits enter, the page updates and now the pge lists
		#"1: Buy peacock feathers" as an item in the todo lists

		inputbox.send_keys(Keys.ENTER)

		time.sleep(1) #use this to avoid StaleElementReferenceException
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		#rows_ref = lambda: table.find_elements_by_tag_name('tr')
		#self.browser.implicitly_wait(3)
		#foundBuy = False
		#for row in rows_ref():
		#	self.browser.implicitly_wait(3)
		#	rows_text = row.text
		#	if (rows_text == '1: Buy peacock feathers'):
		#		foundBuy = True
		#		break
		#if not (foundBuy):
		#	self.fail('Could not find "1: Buy peacock feathers" in rows\' text')
		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

		#There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly" (Edith is very methodical)

		self.browser.implicitly_wait(3)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on her list

		time.sleep(1)
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

		# Edith wonders whether the site will remember her list. Then she sees
		# that the site has generated a unique URL for her -- there is some
		# explanatory text to that effect.

		self.fail('Finish the test!')

		# She visits that URL - her to-do list is still there.

		# Satisfied, she goes back to sleep

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

#if __name__ == '__main__':
#	unittest.main(warnings='ignore')