from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from seleniumwire import webdriver
from util import Util
from sys import platform

class ImageRender:

    def clean_image(self):
        filepath = os.getcwd() + '/captcha.svg'
        url = 'file://' + filepath

        filename = os.path.basename(urlparse(url).path)
        filename_png = os.path.splitext(filename)[0] + '.png'  # change file extension to .png

        chromedriver = os.getcwd() + "/chromedriver"
        if platform == "win32" or platform == "win64":
            chromedriver = os.getcwd() + "/chromedriver.exe"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)

        driver.get(url)

        # Get the width and height of the image
        soup = BeautifulSoup(driver.page_source, 'lxml')
        width = 150
        height = 60
        driver.set_window_size(width, height)  # driver.set_window_size(int(width), int(height))

        driver.save_screenshot(filename_png)
        driver.close()
        driver.quit()
