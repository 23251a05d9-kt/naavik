import json

def lambda_handler(event, context):

    twiml = """
<Response>

<Say voice="alice">
Welcome to Naavik. Your guide to government opportunities.
</Say>

<Say voice="alice">
Press 1 for government jobs.
Press 2 for competitive exams.
</Say>

<Gather numDigits="1" action="https://op57ssrwjtorfm5og5r6mvwvzq0kvzgi.lambda-url.ap-south-1.on.aws/" method="POST">
</Gather>

<Say>No input received. Goodbye.</Say>

</Response>
"""

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/xml"},
        "body": twiml
    }