from twilio.rest import Client
from settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER

client = Client(username=TWILIO_ACCOUNT_SID, password=TWILIO_AUTH_TOKEN)


def send_sms(phone: str, code: str):
    """
    Auth by sms
    """
    client.messages.create(to=phone, from_=TWILIO_NUMBER, body=code)
