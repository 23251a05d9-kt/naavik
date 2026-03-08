import json
import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

TWILIO_NUMBER = "+14754739231"

CALL_HANDLER_URL = "https://demo.twilio.com/welcome/voice/"


def lambda_handler(event, context):

    try:

        body = json.loads(event.get("body", "{}"))
        phone_number = body.get("phone_number")

        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        call = client.calls.create(
            to=phone_number,
            from_=TWILIO_NUMBER,
            url=CALL_HANDLER_URL
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Call initiated",
                "call_sid": call.sid
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }