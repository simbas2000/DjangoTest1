from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):


    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')  #
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('Item 1\n')
        self.check_for_row_in_list_table('1: Item 1')

        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        self.check_for_row_in_list_table('1: Item 1')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('Item 2\n')
        self.check_for_row_in_list_table('1: Item 1')
        self.check_for_row_in_list_table('2: Item 2')