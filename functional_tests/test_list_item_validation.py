from .base import FunctionalTest
import time
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):


    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        self.get_item_input_box().send_keys(Keys.ENTER)

        time.sleep(.2)
        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.assertIn('is-invalid', self.browser.page_source)
        error = self.browser.find_element_by_class_name("invalid-feedback")
        self.assertEqual(error.text, "You can't have an empty list item")

        self.get_item_input_box().send_keys('Item 1' + Keys.ENTER)
        self.check_for_row_in_list_table('1: Item 1')

        self.get_item_input_box().send_keys('')
        self.get_item_input_box().send_keys(Keys.ENTER)

        time.sleep(.2)
        self.check_for_row_in_list_table('1: Item 1')
        error = self.browser.find_element_by_class_name("invalid-feedback")
        self.assertEqual(error.text, "You can't have an empty list item")

        self.get_item_input_box().send_keys('Item 2' + Keys.ENTER)
        time.sleep(.2)
        self.check_for_row_in_list_table('1: Item 1')
        self.check_for_row_in_list_table('2: Item 2')
        
    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('itm1'+Keys.ENTER)
        time.sleep(.2)
        self.check_for_row_in_list_table('1: itm1')
        # User accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('itm1'+Keys.ENTER)
        time.sleep(.2)
        self.check_for_row_in_list_table('1: itm1')
        self.assertIn('is-invalid', self.browser.page_source)
        error = self.browser.find_element_by_class_name("invalid-feedback")
        self.assertEqual(error.text, "You've already got this in your list")

