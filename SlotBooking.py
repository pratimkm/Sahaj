import http.client
from util import Util
import json
from UserSessionManager import UserSessionManager

class SlotBooking:
    def __init__(self):
        self.url = "cdn-api.co-vin.in"
        self.context = "/api/v2/appointment/schedule"
        self.user_agent = Util.user_agent
        self.CAPTCHA_URL = "https://cdn-api.co-vin.in/api/v2/auth/getRecaptcha"

    def book_slot(self, session_id, slot, beneficiaries, captcha):
        bearer_token = ""
        with open('last_jwt_token_id', "r") as f:
            first_line = f.readline()
            tokens = first_line.split(",")
            bearer_token = tokens[1]
            f.close()
        #Force token refresh so that we don't send a stale token
        mydict = {"dose": 1, "session_id": session_id, "slot": slot, "beneficiaries": beneficiaries, "captcha":captcha}
        json_data = json.dumps(mydict)
        headers = {'authorization': 'Bearer ' + bearer_token,
                   'authority': 'cdn-api.co-vin.in',
                   'user-agent': self.user_agent
                   }
        connection = http.client.HTTPSConnection(self.url)
        connection.request(method="POST", url=self.context, body=json_data, headers=headers)
        response = connection.getresponse()
        msg_str = response.read().decode()
        print("###DEBUG### Status Code " + str(response.status) + " & Received Message ==> " + msg_str)
        return response.status

    # def generate_captcha(self, request_header):
    #     print('================================= GETTING CAPTCHA ==================================================')
    #     resp = requests.post(CAPTCHA_URL, headers=request_header)
    #     print(f'Captcha Response Code: {resp.status_code}')
    #
    #     if resp.status_code == 200:
    #         return captcha_builder(resp.json())

# sb = SlotBooking()
# sb.book_slot("8f5c6cef-138b-4be3-893a-6d81b32f446d","03:00PM-04:00PM",["33266433981610","46182911290940"])
