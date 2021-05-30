# Sahaj
Book your covid vaccine slots with ease. Please use this at your own risk. Neither me or nor other repo owners are responsible for usage of this program. Also we do not promise to maintain this code, if you see a bug plz solve it yourself. This had been written in a very short period of time, plz excuse violation of all fundamental coding principles.

Version update for end to end vaccine booking if you have iphone+mac or android+pc. 
You need to enable text message forwarding from your iphone to your linked Mac.Please check this link https://support.apple.com/en-in/HT208386#:~:text=On%20your%20iPhone%2C%20iPad%2C%20or,ID%20on%20all%20your%20devices.
For Android phones we will be using https://messages.google.com/web/ to read sms. Be assured that this happens locally on your machine and nothing is sent to the cloud. We value your privacy.

This has been tested for python 3.8+ . Install dependencies from requirements.txt using pip install requirements.txt . 
Since this program will read the local SQLLite database of imessage app you need to go to system preferences -> security & privacy -> Full Disk Access and add Terminal.


You are free to modify the code for android/pc. This program will run in the background and will check for vaccine slots in your district. 


To run this program you may have to modify the python path in main.py and do chmod +x main.py

To run this program:
./main.py -p <<Your registered mobile no>> -d district_id -b <<comma separated list of beneficiaries>> -n <<type>>
  
  type can be **iphone** or **android**

  
  You can find the list of district ids here https://github.com/bhattbhavesh91/cowin-vaccination-slot-availability/blob/main/district_mapping.csv e.g. Bangalore(BBMP) district id is 294
  You can find beneficiary or reference id once you login to the cowin porta/aarogya setu app


I have taken help from others for quickly solving few problems
https://github.com/bombardier-gif/covid-vaccine-booking
https://github.com/pallupz/covid-vaccine-booking
https://pypi.org/project/imessage-reader/
