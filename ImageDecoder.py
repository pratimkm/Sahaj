from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import PySimpleGUI as sg
import re
from PIL import Image
from bs4 import BeautifulSoup
import json
import base64
import os
import sys

def captcha_builder_auto():
    model = open("model.txt").read()
    html_report_part1 = open("captcha.svg", 'r')
    soup = BeautifulSoup(html_report_part1, 'html.parser')
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
    return CAPTCHA_STRING


captcha_text = captcha_builder_auto()
print('-- Result: {}'.format(captcha_text))

