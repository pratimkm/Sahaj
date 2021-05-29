from sys import platform
import urllib.request
import os.path
import urllib.request
import zipfile


class ChromeDriverDownloader:
    WIN_DOWNLOAD_URL = 'https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_win32.zip'
    MAC_DOWNLOAD_URL = 'https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_mac64.zip'
    LINUX_DOWNLOAD_URL = 'https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip'

    def download_chrome_driver(self):
        chromedriver_url = ChromeDriverDownloader.MAC_DOWNLOAD_URL
        path_to_zip_file = 'chromedriver_mac64.zip'
        if platform == "linux" or platform == "linux2":
            chromedriver_url = ChromeDriverDownloader.LINUX_DOWNLOAD_URL
            path_to_zip_file = 'chromedriver_linux64.zip'
        elif platform == "win32" or platform == "win64":
            chromedriver_url = ChromeDriverDownloader.WIN_DOWNLOAD_URL
            path_to_zip_file = 'chromedriver_win32.zip'

        if os.path.isfile('chromedriver') or os.path.isfile('chromedriver.exe'):
            print("File already exists, not downloading")
        else:
            print('Beginning file download with urllib2...')
            urllib.request.urlretrieve(chromedriver_url, path_to_zip_file)
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                zip_ref.extractall('./')

        if platform == "win32" or platform == "win64":
            os.chmod(os.getcwd() + "/chromedriver.exe", 0o777)
        else:
            os.chmod(os.getcwd() + "/chromedriver", 0o777)