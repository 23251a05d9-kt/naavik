import json
import boto3
import urllib.parse

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("naavik_opportunities")


def get_max_age(max_age_map, category, pwd=False, ex_serviceman=False):

    if not isinstance(max_age_map, dict):
        return max_age_map

    if ex_serviceman and "Ex-Servicemen" in max_age_map:
        ex_map = max_age_map["Ex-Servicemen"]
        if category in ex_map:
            return int(ex_map[category])

    if pwd:
        pwd_key = f"PWD-{category}"
        if pwd_key in max_age_map:
            return int(max_age_map[pwd_key])

    if category in max_age_map:
        return int(max_age_map[category])

    if "UR" in max_age_map:
        return int(max_age_map["UR"])

    return None


def lambda_handler(event, context):

    # Twilio sends data as URL encoded
    body = urllib.parse.parse_qs(event.get("body", ""))

    # Digits = what user typed on keypad
    age = int(body.get("Digits", ["0"])[0])

    # For demo we assume General category
    category = "UR"

    response = table.scan()
    opportunities = response["Items"]

    eligible = []

    for opp in opportunities:

        min_age = opp.get("min_age")
        max_age_map = opp.get("max_age")

        max_age = get_max_age(max_age_map, category)

        if min_age is None or max_age is None:
            continue

        if age >= int(min_age) and age <= int(max_age):

            eligible.append({
                "name": opp.get("name"),
                "organization": opp.get("organization"),
                "deadline": opp.get("deadline"),
                "vacancies": opp.get("vacancies")
            })

    eligible = eligible[:3]

    # Build voice response
    if len(eligible) == 0:

        message = "Sorry. No matching opportunities found."

    else:

        message = "You are eligible for the following opportunities. "

        for opp in eligible:

            message += f"{opp['name']} at {opp['organization']}. "
            message += f"Deadline is {opp['deadline']}. "

    twiml = f"""
<Response>
    <Say voice="alice">{message}</Say>
</Response>
"""

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/xml"
        },
        "body": twiml
    }