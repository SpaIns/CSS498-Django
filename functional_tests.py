from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import unittest
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class NewVisitorTest(unittest.TestCase):

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
		self.browser.get('http://localhost:8000')

		#she notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')

		#she is invited to enter a to-do item straight away

		#She types "buy peacock feather" into a text box

		#When she hits enter, the page updates and now the pge lists
		#"1: Buy peacock feathers" as an item in the todo lists

		#There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly" (Edith is very methodical)

		# The page updates again, and now shows both items on her list

		# Edith wonders whether the site will remember her list. Then she sees
		# that the site has generated a unique URL for her -- there is some
		# explanatory text to that effect.

		# She visits that URL - her to-do list is still there.

		# Satisfied, she goes back to sleep

if __name__ == '__main__':
	unittest.main(warnings='ignore')