from .base import FunctionalTest
import time
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        if 'is-invalid' in self.browser.page_source:
            error = self.browser.find_element_by_class_name("invalid-feedback")
            return error.text
        else:
            return None

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        self.get_item_input_box().send_keys(Keys.ENTER)

        time.sleep(.2)
        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.assertEqual(self.get_error_element(), "You can't have an empty list item")

        self.get_item_input_box().send_keys('Item 1' + Keys.ENTER)
        self.check_for_row_in_list_table('1: Item 1')

        self.get_item_input_box().send_keys('')
        self.get_item_input_box().send_keys(Keys.ENTER)

        time.sleep(.2)
        self.check_for_row_in_list_table('1: Item 1')
        self.assertEqual(self.get_error_element(), "You can't have an empty list item")

        self.get_item_input_box().send_keys('Item 2' + Keys.ENTER)
        time.sleep(.2)
        self.check_for_row_in_list_table('1: Item 1')
        self.check_for_row_in_list_table('2: Item 2')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('itm1' + Keys.ENTER)
        time.sleep(.2)
        self.check_for_row_in_list_table('1: itm1')
        # User accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('itm1' + Keys.ENTER)
        time.sleep(.2)
        self.check_for_row_in_list_table('1: itm1')
        self.assertEqual(self.get_error_element(), "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        time.sleep(.2)
        self.assertIsNotNone(self.get_error_element())

        self.get_item_input_box().send_keys('a')

        time.sleep(.2)
        self.assertIsNone(self.get_error_element())
