from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time

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
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		time.sleep(0.02) #seems needed to avoid bug with selenium (?)

		#User enter items in list using inputbox
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
		inputbox.send_keys('Item 1')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(0.02)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Item 2')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(0.02)
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue( any(row.text == '1: Item 1' for row in rows), "New to-do item(1) did not appear in table!" )
		self.assertTrue( any(row.text == '2: Item 2' for row in rows), "New to-do item(2) did not appear in table!" )


		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')
