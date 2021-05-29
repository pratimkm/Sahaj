from selenium import webdriver
from sys import platform
from ChromedriverDownloader import ChromeDriverDownloader
import os
import time
from util import Util

class AndroidMessageReader:

    def __init__(self):
        ChromeDriverDownloader().download_chrome_driver()
        chromedriver = os.getcwd() + "/chromedriver"
        if platform == "win32" or platform == "win64":
            chromedriver = os.getcwd() + "/chromedriver.exe"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_experimental_option("detach", True)
        capabilities = webdriver.DesiredCapabilities().CHROME
        capabilities['acceptSslCerts'] = True

        # chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(executable_path=chromedriver, desired_capabilities=capabilities)


    def getDriver(self):
        self.driver.get('https://messages.google.com/web')
        time.sleep(60)
        return self.driver

# android = AndroidMessageReader()
# print("Last OTP received : " + android.read_last_otp())