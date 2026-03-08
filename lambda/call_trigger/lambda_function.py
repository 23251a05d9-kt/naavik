import json
from twilio.rest import Client

ACCOUNT_SID = "AC6144cc475224e624f33953010e8433d7"
AUTH_TOKEN = "c44ac368c2c318946278abac977a9279"

TWILIO_NUMBER = "+14754739231"

CALL_HANDLER_URL = "https://fklktib2fxjoarvwbpbm5c7rui0ldiwl.lambda-url.ap-south-1.on.aws/"


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