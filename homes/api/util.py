from django.conf import settings
import requests


def send_signup_email(email, link_text):
    domain = settings.MAILGUN_DOMAIN
    result = requests.post(
        "https://api.mailgun.net/v3/" + domain + "/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "OpenHouse API <" + settings.MAILGUN_API_FROM + ">",
              "to": [email],
              "subject": "OpenHouse API Account Confirmation",
              "text": "Click to Verify your account: " + link_text})

    print(result.text)

