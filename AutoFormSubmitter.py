from seleniumwire import webdriver
import time
import json
import signal
import os


class AutoFormSubmitter:

    def submitOTPRequest(self,phone_number):
        chromedriver = "/Users/anwesabagchi/Downloads/chromedriver"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        driver = webdriver.Chrome(executable_path=chromedriver)

        driver.get('https://selfregistration.cowin.gov.in/')
        pid = driver.service.process.pid
        time.sleep(2)
        username_input = '//*[@id="mat-input-0"]'
        driver.find_element_by_xpath(username_input).send_keys("9945184400")
        login_submit = '//*[@id="main-content"]/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[1]/ion-grid/form/ion-row/ion-col[2]/div/ion-button'
        driver.find_element_by_xpath(login_submit).click()
        time.sleep(2)

        txnID = ''
        # Access requests via the `requests` attribute
        for request in driver.requests:
            if request.response and request.url.find("generateMobileOTP") != -1:
                resp = json.loads(request.response.body.decode('utf-8'))
                txnID = resp.get("txnId")
                print("Received txnId : " + txnID)
                with open('last_txn_id', "w") as f:
                    f.write(txnID)
                    f.close()
                    break

        driver.close()
        driver.quit()

        return txnID


