import json
import datetime
import http.client
import logging
from util import Util
# http.client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

class Availability_Checker:
    def __init__(self,district_id):
        self.district_id = district_id
        day1 = datetime.date.today() #+ datetime.timedelta(days=1)
        self.day1 = day1.strftime("%d-%m-%Y")
        self.url = "cdn-api.co-vin.in"
        self.context1 = "/api/v2/appointment/sessions/calendarByDistrict?district_id="+str(district_id)+"&date="+self.day1
        self.user_agent = Util.user_agent
        self.request_body = {}

    def location_availability(self):
        resp = None
        try:
            connection = http.client.HTTPSConnection(self.url)
            with open('last_jwt_token_id') as f:
                first_line = f.readline()
                tokens = first_line.split(",")
                bearer_token = tokens[1]
                headers = {'authorization': 'Bearer ' + bearer_token,
                           'authority': 'cdn-api.co-vin.in',
                           'user-agent': self.user_agent
                           }
                connection.request("GET", self.context1, headers=headers)
                response = connection.getresponse()
                msg_str = response.read().decode()

                if response.status == 200:
                    resp = json.loads(msg_str)
                    for center in resp['centers']:
                        for session in center['sessions']:
                            if session['available_capacity'] > 0 and session['min_age_limit'] < 45 and session[
                                'available_capacity_dose1'] > 5:
                                print(str(center['pincode']) + " have " + str(
                                    session['available_capacity']) + " slots opened for age group " + str(
                                    session['min_age_limit']))
                                available_slots = session['slots']
                                return center['pincode'], session['session_id'], available_slots
                else:
                    print("###DEBUG### Status Code " + str(response.status) + " & Received Message ==> " + msg_str)
                print("No slots available in your district at : " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        except:
            print("Received data error, will continue")

        return "","",""

# av = Availability_Checker(294)
# pincode,session,available_slot = av.location_availability()
# print("Vaccine slot available at : " + str(pincode) + " for available slot : " + available_slot + " for session_id : " + session)