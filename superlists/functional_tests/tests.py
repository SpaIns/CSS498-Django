from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

#import unittest
import time
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class NewVisitorTest(StaticLiveServerTestCase):

	def setUp(self):
		binary = FirefoxBinary(r'/home/spa/firefox/firefox') 
		self.browser = webdriver.Firefox(firefox_binary=binary)
		#self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.refresh()
		self.browser.quit()

	def test_can_start_a_list_for_one_user(self):
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

		#When she hits enter, she is taken to a new url and now 
		#the page lists "1: Buy peacock feathers" as an item 
		#in the todo lists

		inputbox.send_keys(Keys.ENTER)
		#edith_list_url = self.browser.current_url
		#self.assertRegex(edith_list_url, '/lists/.+')
		time.sleep(1)
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		time.sleep(1) #use this to avoid StaleElementReferenceException

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

		#satisfied, she goes back to sleep

	def test_multiple_users_can_start_lists_at_different_urls(self):

		# Edith starts a new todo list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)

		time.sleep(1)
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		# She notices her list has a unique url
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		# Now a new user, francis comes along to the site.

		## We use a new browser session to make sure no information of
		## Edith's is coming through from cookies etc
		self.browser.quit()
		binary = FirefoxBinary(r'/home/spa/firefox/firefox') 
		self.browser = webdriver.Firefox(firefox_binary=binary)

		# Francis visits the home page. There is no sign of Edith's
		# list.
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# Francis starts a new list by entering an item. He is
		# less interesting than Edith...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		time.sleep(1)
		# Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		#Again, there is no trace of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		#self.fail('Finish the test!')

		# She visits that URL - her to-do list is still there.

		# Satisfied, They both go back to sleep


	def test_layout_and_styling(self):
		#Edith goes to the home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		#She notices the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=5
		)

		#She starts a new list and sees the input is nicely
		# centered there too
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=20
		)

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

#if __name__ == '__main__':
#	unittest.main(warnings='ignore')
