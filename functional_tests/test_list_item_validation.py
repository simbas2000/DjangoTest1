from .base import FunctionalTest
import time
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):


    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        time.sleep(.2)
        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        error = self.browser.find_element_by_class_name("invalid-feedback")
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('Item 1' + Keys.ENTER)
        self.check_for_row_in_list_table('1: Item 1')

        self.browser.find_element_by_id('id_new_item').send_keys('')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        time.sleep(.2)
        self.check_for_row_in_list_table('1: Item 1')
        error = self.browser.find_element_by_class_name("invalid-feedback")
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('Item 2' + Keys.ENTER)
        self.check_for_row_in_list_table('1: Item 1')
        self.check_for_row_in_list_table('2: Item 2')