#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3

import time
from UserSessionManager import UserSessionManager
from Availability_Checker import Availability_Checker
import threading
from SlotBooking import SlotBooking
from util import Util
import requests
from captcha import CaptchaSolver
import sys, getopt

def refresh_user_session(mobile_no):
    while True:
        UserSessionManager(mobile_no).create_jwt_token()
        time.sleep(Util.login_refresh_period)     # Token refreshed every 12 minute
        continue

def check_vaccine_availability(district_id,beneficiaries):
    CAPTCHA_URL = "https://cdn-api.co-vin.in/api/v2/auth/getRecaptcha"

    while True:
        pincode,session_id,slots = Availability_Checker(district_id).location_availability()
        # check if task is done
        if pincode != "":
            bearer_token = ""
            with open('last_jwt_token_id', "r") as f:
                first_line = f.readline()
                tokens = first_line.split(",")
                bearer_token = tokens[1]
                f.close()
            resp = requests.post(CAPTCHA_URL, headers={'authorization': 'Bearer ' + bearer_token,
                                                       'authority': 'cdn-api.co-vin.in',
                                                       'user-agent': Util.user_agent
                                                       })
            print(f'Captcha Response Code: {resp.status_code}')
            if resp.status_code == 200:
                captcha = CaptchaSolver().captcha_builder_auto(resp.json())
                print("Decoded captcha : " + captcha)
                for slot in slots:
                    status_code = SlotBooking().book_slot(session_id, slot, beneficiaries, captcha)
                    if status_code == 200:
                        break
            else:
                print("Failed to retrieve captcha")
                return resp.status

        time.sleep(10)


if __name__ == '__main__':
    phone_number = ''
    beneficiaries =  []
    district_id = 294
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:d:b", ["phone=", "district=","beneficiaries="])
    except getopt.GetoptError:
        print('test.py -p <10 digit mobile number> -d <district id> -b <comma separated list of beneficiaries>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--phone"):
            phone_number = arg
        elif opt in ("-d", "--district"):
            district_id = arg
        elif opt in ("-b", "--beneficiaries"):
            beneficiaries = arg.split(",")
    print('Phone number is ' +  phone_number)
    print('District Id is ' + str(district_id))
    for beneficiary in beneficiaries:
        print('Beneficiaries are ' + beneficiary)
    # creating thread
    t1 = threading.Thread(target=refresh_user_session, args=(phone_number,))
    # starting thread 1
    t1.start()

    time.sleep(10)

    t2 = threading.Thread(target=check_vaccine_availability, args=(district_id,beneficiaries))
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

    # both threads completely executed
    print("Done!")
