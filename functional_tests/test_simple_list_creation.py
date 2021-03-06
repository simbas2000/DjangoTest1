from .base import FunctionalTest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrive_it_later(self):
        # User visits homepage
        self.browser.get(self.server_url)

        # User notices title and header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        time.sleep(0.02)  # seems needed to avoid bug with selenium (?)

        # User enter items in list using inputbox
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('Item 1')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.2)
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Item 1')
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Item 2')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.2)
        self.check_for_row_in_list_table('2: Item 2')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Item 1', page_text)
        self.assertNotIn('2: Item 2', page_text)

        inputbox = self.get_item_input_box()
        inputbox.send_keys('l2_i1')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.4)

        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user_list_url, user2_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Item 1', page_text)
        self.assertIn('l2_i1', page_text)

