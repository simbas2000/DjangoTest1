from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrive_it_later(self):
		#User visits homepage
		self.browser.get('http://localhost:8000')

		#User notices title and header
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

#User notices the page title and header mention to-do lists
assert 'To-Do' in browser.title

#User insert To-Do items in list
#Unique URL
#Check URL

browser.quit()
