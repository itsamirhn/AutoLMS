import os
import pickle

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class LMSDriver:

    def __init__(self, chromedriver: str, username: str, password: str, base_url: str, cookies_path: str = None):
        self.username = username
        self.password = password
        self.base_url = base_url
        option = ChromeOptions()
        option.add_experimental_option('detach', True)
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
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

    @property
    def course_url(self) -> str:
        return self.base_url + '/course/view.php'

    def get_course_url(self, course_id):
        return self.course_url + '?id={}'.format(course_id)

    def save_cookies(self):
        with open(self.cookies_path, 'wb') as f:
            pickle.dump(self.driver.get_cookies(), f)

    def load_cookies(self, redirect_url=None):
        if not os.path.exists(self.cookies_path):
            if redirect_url:
                self.go(redirect_url)
            return
        self.go(self.base_url)
        self.driver.delete_all_cookies()
        with open(self.cookies_path, 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        if redirect_url:
            self.go(redirect_url)

    def click(self, by: str, value: str = None, timeout: int = 10):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(expected_conditions.element_to_be_clickable((by, value))).click()

    def click_text(self, text, timeout: int = 10):
        self.click(By.XPATH, "//*[contains(text(), '{}')]".format(text), timeout)

    def click_text_multiple(self, text1, text2, timeout: int = 10):
        self.click(By.XPATH, "//*[contains(text(), '{}') or contains(text(), '{}')]".format(text1, text2), timeout)

    def go(self, url):
        self.driver.get(url)
        if self.driver.current_url != url:
            self.login()
        self.driver.get(url)

    def login(self):
        if not self.username or not self.password:
            raise Exception('No login credentials!')
        if len(self.driver.find_elements(By.XPATH, "//a[contains(text(), 'سامیا')]")) > 0:
            redirect = self.driver.find_element(By.XPATH, "//a[contains(text(), 'سامیا')]")
            redirect.click()
        self.driver.find_element(By.XPATH, "//input[@id='username' or @name='name']").send_keys(self.username)
        self.driver.find_element(By.XPATH, "//input[@id='password' or @name='pass']").send_keys(
            self.password + Keys.RETURN)
        if self.driver.current_url == self.login_url:
            raise Exception('Invalid credentials!')
        self.save_cookies()

    def go_to_my(self):
        self.go(self.my_url)

    def go_to_last_event(self):
        if self.driver.current_url != self.my_url:
            self.go_to_my()
        self.click(By.CSS_SELECTOR, 'a[data-type="event"]')
        self.click_text_multiple('رفتن به فعالیت', 'Go to activity')
        if 'adobeconnect' in self.driver.current_url:
            self.go_to_adobeconnect()
        else:
            raise Exception('Not implemented yet!')

    def go_to_adobeconnect(self, browser: bool = True):
        if 'adobeconnect' not in self.driver.current_url:
            raise Exception('Driver is not on Adobe Connect event!')
        self.click(By.CLASS_NAME, 'aconbtnjoin')
        self.driver.switch_to.window(self.driver.window_handles[1])
        wait = WebDriverWait(self.driver, 30)
        button = wait.until(expected_conditions.element_to_be_clickable(
            (By.CSS_SELECTOR, 'div.open-in-{}-button div.button-content'.format('browser' if browser else 'app'))))
        action = ActionChains(self.driver)
        action.move_to_element(button).click().perform()
        if not browser:
            return
        self.driver.maximize_window()
        iframe = wait.until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, 'iframe[name=html-meeting-view-frame]')
        ))
        self.driver.switch_to.frame(iframe)
        self.click(By.CLASS_NAME, "spectrum-Button--secondary", 30)

    def go_to_onlineclass(self, browser: bool = True):
        if 'online' not in self.driver.current_url:
            raise Exception('Driver is not on Onlineclass event!')
        self.click(By.CSS_SELECTOR, 'input[name=submitbutton]')
        wait = WebDriverWait(self.driver, 30)
        button = wait.until(expected_conditions.element_to_be_clickable(
            (By.CSS_SELECTOR, 'div.open-in-{}-button div.button-content'.format('browser' if browser else 'app'))))
        action = ActionChains(self.driver)
        action.move_to_element(button).click().perform()
        if not browser:
            return
        self.driver.maximize_window()
        iframe = wait.until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, 'iframe[name=html-meeting-view-frame]')
        ))
        self.driver.switch_to.frame(iframe)
        self.click(By.CLASS_NAME, "spectrum-Button--secondary", 30)

    def go_to_course(self, course_id):
        self.go(self.get_course_url(course_id))

    def go_to_course_last_event(self, course_id):
        self.go_to_course(course_id)
        self.click(By.XPATH,
                   "//li[(contains(@class,'adobeconnect') or contains(@class,'onlineclass')) and not(contains(., 'رزرو'))][last()]//a")
        if 'adobeconnect' in self.driver.current_url:
            self.go_to_adobeconnect()
        elif 'onlineclass' in self.driver.current_url:
            self.go_to_onlineclass()
        else:
            raise Exception('Not implemented yet!')


def check(self):
    # TODO: Check last event exist or not!
    self.go_to_last_event()
