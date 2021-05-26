from twocaptcha import TwoCaptcha
from ImageRender import ImageRender
import re
from bs4 import BeautifulSoup
import json
import base64

class CaptchaSolver:

    def captcha_builder(self,resp):
        with open('captcha.svg', 'w') as f:
            f.write(re.sub('(<path d=)(.*?)(fill=\"none\"/>)', '', resp['captcha']))
            f.close()

        # drawing = svg2rlg('captcha.svg')
        ## This method renders a clean image
        ImageRender().clean_image()
        solver = TwoCaptcha('c8702162316fdbe73da0f795f6565e')
        raw_data = solver.normal('captcha.png', caseSensitive=1)
        captcha_code = raw_data.get("code")
        print("Solved Captcha : " + captcha_code)
        return captcha_code

    def captcha_builder_auto(self,resp):
        model = open("model.txt").read()
        soup = BeautifulSoup(resp['captcha'], 'html.parser')
        model = json.loads(base64.b64decode(model.encode('ascii')))
        CAPTCHA = {}

        for path in soup.find_all('path', {'fill': re.compile("#")}):
            ENCODED_STRING = path.get('d').upper()
            INDEX = re.findall('M(\d+)', ENCODED_STRING)[0]
            ENCODED_STRING = re.findall("([A-Z])", ENCODED_STRING)
            ENCODED_STRING = "".join(ENCODED_STRING)
            CAPTCHA[int(INDEX)] = model.get(ENCODED_STRING)

        CAPTCHA = sorted(CAPTCHA.items())
        CAPTCHA_STRING = ''

        for char in CAPTCHA:
            CAPTCHA_STRING += char[1]
        #For debugging
        with open('captcha.svg', 'w') as f:
            f.write(re.sub('(<path d=)(.*?)(fill=\"none\"/>)', '', resp['captcha']))
            f.close()
        ImageRender().clean_image()

        return CAPTCHA_STRING.strip()

    # layout = [[sg.Image('captcha.png')],
    #           [sg.Text("Enter Captcha Below")],
    #           [sg.Input(key='inp')],
    #           [sg.Button('Submit', bind_return_key=True)]]
    #
    # window = sg.Window('Enter Captcha', layout, finalize=True)
    # window.TKroot.focus_force()         # focus on window
    # window.Element('inp').SetFocus()    # focus on field
    # event, values = window.read()
    # window.close()
    # return values['inp']