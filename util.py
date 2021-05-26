import json
import http.client
# import logging
# http.client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

class Util:
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    mobile_no = "9945184400"
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
