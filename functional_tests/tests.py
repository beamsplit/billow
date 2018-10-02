import time
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import unittest

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('/Users/beamsplit/Documents/BILLOW/VM/billow/chromedriver')
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.driver.quit()
    
    def test_layout_and_styling(self):
        # Alice goes to the home page
        self.driver.get('%s%s' % (self.live_server_url,'/home'))
        self.driver.set_window_size(1024, 768)
        
        # She notices the header text is nicely centered
        header_text = self.driver.find_element_by_tag_name('h1')
        self.assertAlmostEqual(
                               header_text.location['x'] + header_text.size['width'] / 2,
                               512,
                               delta=10
                               )

    def test_can_see_home_page(self):

        # Alice has heard about an app that will let her follow legislation that she cares about.
        # She goes to check it out, opening the home page.

        self.driver.get('%s%s' % (self.live_server_url,'/home'))
        self.assertIn( 'Home', self.driver.title)
        
        # She sees the header.
        
        header_text = self.driver.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'FOLLOW LEGISLATION YOU CARE ABOUT.')


        # She sees the invitation to "Get Started" and decides to see where it takes her.
        # She sees the Bills page load and notices the header 'Bills'

        # She scrolls down and sees the different bills, with their titles and tags.

        # Alice, as a physician, is very interested in healthcare legislation. She clicks on the 'Health' tag.


    def test_register_for_app(self):

        # Alice decides she likes the site and wants to create an account.
        # She navigates to the Register page.

        self.driver.get('%s%s' % (self.live_server_url,'/accounts/signup/citizen/'))
        time.sleep(3)

        # She is invited to enter her information.

        input_username = self.driver.find_element_by_id('id_username')
        self.assertEqual(input_username.get_attribute('placeholder'),'Username')

        # She enters a username 'Alice'

        input_username.send_keys('Alice')

        # She chooses her location as Ireland (value 2).

        input_location = Select(self.driver.find_element_by_id('id_location'))
        input_location.select_by_value('2')
        #self.assertEqual(input_location, '2')
        
        

        # She chooses her password '12345pwd' and confirms it.

        input_password1 = self.driver.find_element_by_id('id_password1')
        input_password1.send_keys('12345pwd')

        input_password2 = self.driver.find_element_by_id('id_password2')
        input_password2.send_keys('12345pwd')

        # She chooses her preferred category, 'Media'.
        
        ##### THIS PART DOESN"T LOAD IN LIVESERVER
        
        #input_tag = self.driver.find_element_by_id('id_interests_0')
        #input_tag.click()
        #self.assertTrue(self.driver.find_element_by_id('id_interests_0').is_selected() )

        # She submits the form.

        input_submit = self.driver.find_element_by_id('id_submit_signup').submit()
        time.sleep(5)

        self.assertIn('Profile', self.driver.title)


if __name__ == '__main__':
    unittest.main()
