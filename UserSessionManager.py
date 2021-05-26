import http.client
import fetch_data
from datetime import datetime
import re
from collections import OrderedDict
import time
import json
import hashlib
from AutoFormSubmitter import AutoFormSubmitter
from util import Util
import logging
# http.client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


class UserSessionManager:
    def __init__(self, mobile_number):
        self.url = "cdn-api.co-vin.in"
        self.mobile_number = mobile_number
        self.user_agent = Util.user_agent

    def create_jwt_token(self):
        tokens = ["",""]
        with open('last_jwt_token_id', "r") as f:
            first_line = f.readline()
            tokens = first_line.split(",")
            f.close()

        last_written_time = 100000
        if tokens[0] != "":
            last_written_time = datetime.strptime(tokens[0], '%Y-%m-%d %H:%M:%S')
            datetime_diff = datetime.now() - last_written_time
            last_written_time = datetime_diff.total_seconds()

        if last_written_time > Util.login_refresh_period:        #else token is valid
            time_diff, last_otp, txnId = self.sendOTPRequest()
            try:
                token_rcvd = self.enter_otp(last_otp, txnId)
                with open('last_jwt_token_id', "w") as f:
                    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "," + token_rcvd)
                    f.close()
                print("Completed writing new token : " + token_rcvd)
            except:
                print("Got exception while entering OTP, loop continues")
            finally:
                return
        else:
            print("Token is valid, not writing again")

    def check_last_otp_txnId(self):
        fd = fetch_data.FetchData()
        my_data = fd.get_messages()
        mydict = {}
        for p in my_data:
            recv_otp = self.parse_otp_message(p[1])
            if recv_otp == -1:
                return 1000,00000,""
            mydict[datetime.strptime(p[2], '%Y-%m-%d %H:%M:%S')] = self.parse_otp_message(p[1])

        mydict = OrderedDict(sorted(mydict.items(), reverse=True))
        datetime_diff = datetime.now() - list(mydict.keys())[0]
        last_otp = list(mydict.values())[0]
        first_line = ""
        with open('last_txn_id', "r") as f:
            first_line = f.readline()
            f.close()
        return datetime_diff.total_seconds(),last_otp,first_line

    def sendOTPRequest(self):
        time_diff, last_otp, txnId = self.check_last_otp_txnId()
        if time_diff > 175: ## Send request if its past 3 minutes
            AutoFormSubmitter().submitOTPRequest(phone_number=self.mobile_number)
            for i in range(0,60):   ## Wait for OTP upto 1 minute
                time.sleep(2)
                time_diff, last_otp, txnId = self.check_last_otp_txnId()
                if time_diff < 175:
                    return time_diff, last_otp, txnId
        return time_diff, last_otp, txnId

    def enter_otp(self,otp,txnId):
        confirm_input = {'otp' : hashlib.sha256(str(otp).encode()).hexdigest(), 'txnId' : txnId}
        confirm_json = json.dumps(confirm_input)
        resp = Util().get_post_response(self.url,confirm_json,"/api/v2/auth/validateMobileOtp")
        token_rcvd = resp.get("token")
        return token_rcvd

    def parse_otp_message(self,message):
        km = re.search('[0-9][0-9][0-9][0-9][0-9][0-9]',message)
        if km is not None:
            return re.search('[0-9][0-9][0-9][0-9][0-9][0-9]',message).group(0)
        else:
            -1


    def print_beneficiaries(self,bearer_token):
        connection = http.client.HTTPSConnection(self.url)
        headers = {'authorization': 'Bearer ' + bearer_token,
                   'authority' : 'cdn-api.co-vin.in',
                   'origin' : 'https://selfregistration.cowin.gov.in',
                   'user-agent': self.user_agent
                   }

        connection.request("GET", "/api/v2/appointment/beneficiaries",headers=headers)
        response = connection.getresponse()
        msg_str = response.read().decode()
        # print("###DEBUG### Status Code " + str(response.status) + " & Received Message ==> " + msg_str)
        resp = json.loads(msg_str)


# sm = UserSessionManager("9945184400")
# sm.create_jwt_token()
