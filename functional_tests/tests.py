import sys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
            super().setUpClass()
            cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrive_it_later(self):
        #User visits homepage
        self.browser.get(self.server_url)
        
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
        time.sleep(0.2)
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Item 1')
        inputbox = self.browser.find_element_by_id('id_new_item')
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

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('l2_i1')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.8)

        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user_list_url, user2_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Item 1', page_text)
        self.assertIn('l2_i1', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5
        )

        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5
        )
