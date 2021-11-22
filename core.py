import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import pickle
import os


class LMSDriver:

    def __init__(self, chromedriver: str, username: str, password: str, base_url: str = 'https://lms.khu.ac.ir',
                 cookies_path: str = None):
        self.username = username
        self.password = password
        self.base_url = base_url
        option = ChromeOptions()
        option.add_experimental_option('detach', True)
        self.driver = Chrome(executable_path=chromedriver, chrome_options=option)
        if not cookies_path:
            cookies_path = '{}_cookies.pkl'.format(username)
        self.cookies_path = cookies_path

    @property
    def login_url(self) -> str:
        return self.base_url + '/login/index.php'

    @property
    def my_url(self) -> str:
        return self.base_url + '/my/'

    def save_cookies(self):
        with open(self.cookies_path, 'wb') as f:
            pickle.dump(self.driver.get_cookies(), f)

    def load_cookies(self, redirect_url=None):
        if not os.path.exists(self.cookies_path):
            if redirect_url:
                self.driver.get(redirect_url)
            return
        self.driver.get(self.base_url)
        self.driver.delete_all_cookies()
        with open(self.cookies_path, 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        if redirect_url:
            self.driver.get(redirect_url)

    def click(self, by: str, value: str = None, timeout: int = 10):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(expected_conditions.element_to_be_clickable((by, value))).click()

    def click_text(self, text):
        self.click(By.XPATH, '//*[text() = "{}"]'.format(text))

    def login(self):
        if not self.username or not self.password:
            raise Exception('No login credentials!')
        self.driver.get(self.login_url)
        self.driver.find_element(By.ID, 'username').send_keys(self.username)
        self.driver.find_element(By.ID, 'password').send_keys(self.password + Keys.RETURN)
        if self.driver.current_url != self.my_url:
            raise Exception('Invalid credentials!')
        self.save_cookies()

    def go_to_my(self):
        self.load_cookies(self.my_url)
        if self.driver.current_url == self.login_url:
            self.login()

    def go_to_last_event(self):
        if self.driver.current_url != self.my_url:
            self.go_to_my()
        self.click(By.CSS_SELECTOR, 'a[data-type="event"')
        self.click_text('رفتن به فعالیت')
        if 'adobeconnect' in self.driver.current_url:
            self.go_to_adobeconnect()
        else:
            raise Exception('Not implemented yet!')

    def go_to_adobeconnect(self, browser: bool = True):
        if not 'adobeconnect' in self.driver.current_url:
            raise Exception('Driver is not on Adobe Connect event!')
        self.click(By.CLASS_NAME, 'aconbtnjoin')
        self.driver.switch_to.window(self.driver.window_handles[1])
        wait = WebDriverWait(self.driver, 20)
        button = wait.until(expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.open-in-{}-button div.button-content'.format('browser' if browser else 'app'))))
        action = ActionChains(self.driver)
        action.move_to_element(button).click().perform()

    def check(self):
        # TODO: Check last event exist or not!
        self.go_to_last_event()
