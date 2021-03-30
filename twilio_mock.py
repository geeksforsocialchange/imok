import requests
import argparse

ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-f", "--from", required=True,
   help="e164 phone number")
ap.add_argument("-m", "--message", required=True,
   help="incoming message")
args = vars(ap.parse_args())

files = {
    'AccountSid': (None, '123'),
    'Body': (None, args['message']),
    'FromState': (None, '123'),
    'MessageSid': (None, '123'),
    'From': (None, args['from']),
    'FromCountry': (None, '123'),
    'FromCity': (None, '123'),
    'FromZip': (None, '123'),
    'To': (None, '123'),
    'MessagingServiceSid': (None, '123'),
    'NumMedia': (None, '123'),
}

response = requests.post('http://localhost:8000/application/twilio', files=files)
print(response.status_code)
print(response.content)