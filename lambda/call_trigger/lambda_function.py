import json
import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = os.environ["TWILIO_PHONE_NUMBER"]

client = Client(account_sid, auth_token)


def lambda_handler(event, context):

    body = json.loads(event["body"])

    phone = body["phone"]

    call = client.calls.create(

        to=phone,

        from_=twilio_number,

        url="YOUR_CALL_HANDLER_LAMBDA_URL"

    )

    return {
        "statusCode":200,
        "headers":{
            "Access-Control-Allow-Origin":"*",
            "Content-Type":"application/json"
        },
        "body":json.dumps({
            "message":"Call initiated successfully"
        })
    }