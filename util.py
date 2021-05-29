import json
import http.client
import re
import time
import datetime
# import logging
# http.client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

class Util:
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    login_refresh_period = 720  # every 12 minute
    def get_post_response(self, url1, json_data, context):
        user_agent = Util.user_agent
        conn = http.client.HTTPSConnection(url1)
        headers = {'Content-type': 'application/json',
                   'origin': 'https://selfregistration.cowin.gov.in',
                   'user-agent': user_agent
                   }
        if json_data == None:
            conn.request('POST', context, headers=headers)
        else:
            conn.request('POST', context, json_data, headers)
        response = conn.getresponse()
        # print("###DEBUG### Received response code ==>> " + str(response.status) + " for URL ==>> " + context)
        if response.status != 200:
            return ""
        msg_str = response.read().decode()
        # print("###DEBUG### Received Message ==> " + msg_str)
        resp = json.loads(msg_str)
        return resp

    def parse_otp_message(self,message):
        km = re.search('[0-9][0-9][0-9][0-9][0-9][0-9]',message)
        if km is not None:
            return re.search('[0-9][0-9][0-9][0-9][0-9][0-9]',message).group(0)
        else:
            -1

    def read_last_otp(self,drv):
        drv.find_element_by_xpath("//*[text()='AX-NHPSMS']").click()
        time.sleep(2)
        # otp_message = drv.find_elements_by_class_name('text-msg')[-1].text
        # last_msgtag = drv.find_elements_by_class_name("ng-trigger ng-trigger-incomingMessage ng-tns-c153-134 ng-star-inserted")[-1]
        last_msgtag = drv.find_element_by_xpath("//*/mws-message-wrapper[last()]/div/div/div/mws-message-part-router/mws-text-message-part")
        last_msgs = last_msgtag.get_attribute("aria-label")
        print("Received OTP message : " + last_msgs)
        last_msgs_arr = last_msgs.split(".")
        otp = last_msgs_arr[0][-6:]
        last_received_date = datetime.datetime.strptime(last_msgs_arr[3].replace(" Received on ",""),"%b %d, %Y at %I:%M %p")
        receive_time = datetime.datetime.now() - last_received_date
        return receive_time.total_seconds(), otp