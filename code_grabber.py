from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import elements as e
import generator
import code
import time


class Driver:
    def __init__(self, path, args, driver_path):
        self.service = Service(driver_path)
        options = Options()
        options.binary_location = path
        for arg in args:
            options.add_argument(arg)
        self.options = options

    def create_driver(self):
        driver = webdriver.Firefox(service=self.service, options=self.options)
        driver.set_window_size(1200, 800)
        return driver


class CodeGrabber:
    def __init__(self):
        dr_path = r'C:\\Program Files\\Mozilla Firefox\\geckodriver.exe'
        path = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        args = ["--disable-gpu", "--disable-logging"]
        driver = Driver(path=path, args=args, driver_path=dr_path)
        self.wdriver = driver.create_driver()

    def wait(self, elem, delay):
        try:
            elem = WebDriverWait(self.wdriver, delay).until(EC.presence_of_element_located((By.XPATH, elem)))
            return elem
        except TimeoutException:
            print('Timed Out!')

    def fill(self, elem, text=None):
        element = CodeGrabber.wait(self, elem, 30)
        element.click()
        if text is not None:
            element.send_keys(text)
        # time.sleep(3)

    def getcode(self):
        self.wdriver.get(e.start_page)

        CodeGrabber.fill(self, e.register_button)
        CodeGrabber.fill(self, e.select_plan)

        email = generator.gen_email()
        # print(email)
        CodeGrabber.fill(self, '//*[@id="email"]', email)
        password = generator.gen(16)
        # print(password)
        CodeGrabber.fill(self, '//*[@id="password"]', password)
        CodeGrabber.fill(self, '//*[@id="firstName"]', generator.gen(16))

        CodeGrabber.fill(self, e.month_sel)
        CodeGrabber.fill(self, '//*[@id="birthdayMonth-item-0"]')

        CodeGrabber.fill(self, e.day_sel)
        CodeGrabber.fill(self, '//*[@id="birthdayDay-item-4"]')

        CodeGrabber.fill(self, e.year_sel)
        CodeGrabber.fill(self, '//*[@id="birthdayYear-item-24"]')

        CodeGrabber.fill(self, e.gender_sel)
        CodeGrabber.fill(self, '//*[@id="gender-item-1"]')

        CodeGrabber.fill(self, e.continue_button)
        time.sleep(7)

        self.wdriver.get(e.promo_page)

        CodeGrabber.fill(self, e.login_button)
        CodeGrabber.fill(self, e.get_code)
        CodeGrabber.fill(self, e.popup)

        for _ in range(20):
            try:
                self.wdriver.switch_to.window(self.wdriver.window_handles[1])
            except IndexError:
                time.sleep(1)

        time.sleep(3)
        url = self.wdriver.current_url

        promo = code.get_code(url)

        with open('codes.txt', 'a') as f:
            f.write(promo)

        print(promo)

        self.wdriver.delete_all_cookies()
        self.wdriver.quit()


code_grabber = CodeGrabber()
while True:
    code_grabber.getcode()
