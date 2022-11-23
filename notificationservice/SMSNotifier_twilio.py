# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Find your Account SID and Auth Token in Account Info and set the environment variables.
# See http://twil.io/secure


class SMSNotifier_twilio:
    def __init__(self, sid, token, sender):
        self.__sid = sid
        self.__token = token
        self.__sender = sender

        self.__client = None

    def __enter__(self):
        client = Client(self.__sid, self.__token)
    
    def send(self, info):
        phone_number = info.phone
        message = 'Your queue is ready'

        text = client.messages.create(
            body= message,
            from_= self.__sender,
            to= phone_number
        )

        
