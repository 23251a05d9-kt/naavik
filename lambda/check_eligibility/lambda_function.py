import json
import boto3
import urllib.parse
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("naavik_opportunities")


def get_max_age(max_age_map, category):

    if isinstance(max_age_map, Decimal):
        return int(max_age_map)

    if isinstance(max_age_map, (int,str)):
        return int(max_age_map)

    if not isinstance(max_age_map, dict):
        return None

    if category in max_age_map:

        value=max_age_map[category]

        if isinstance(value,Decimal):
            return int(value)

        if isinstance(value,(int,str)):
            return int(value)

        if isinstance(value,dict) and "N" in value:
            return int(value["N"])

    if "UR" in max_age_map:

        value=max_age_map["UR"]

        if isinstance(value,Decimal):
            return int(value)

        if isinstance(value,(int,str)):
            return int(value)

        if isinstance(value,dict) and "N" in value:
            return int(value["N"])

    return None


def lambda_handler(event, context):

    body=urllib.parse.parse_qs(event.get("body",""))

    digits=body.get("Digits",["0"])[0]

    try:
        age=int(digits)
    except:
        age=0

    category="UR"

    response=table.scan()

    opportunities=response["Items"]

    eligible=[]

    for opp in opportunities:

        min_age=opp.get("min_age")

        max_age_map=opp.get("max_age")

        if min_age is None or max_age_map is None:

            eligible.append({

                "name":opp.get("name"),

                "organization":opp.get("organization"),

                "deadline":opp.get("deadline"),

                "vacancies":opp.get("vacancies")

            })

            continue


        max_age=get_max_age(max_age_map,category)

        if max_age is None:
            continue

        if age>=int(min_age) and age<=int(max_age):

            eligible.append({

                "name":opp.get("name"),

                "organization":opp.get("organization"),

                "deadline":opp.get("deadline"),

                "vacancies":opp.get("vacancies")

            })

    eligible=eligible[:3]

    if len(eligible)==0:

        message="Sorry. No matching opportunities found."

    else:

        message="You are eligible for the following opportunities. "

        for opp in eligible:

            name=opp.get("name") or "an opportunity"

            org=opp.get("organization")

            deadline=opp.get("deadline")

            message+=f"{name}. "

            if org:
                message+=f"Offered by {org}. "

            if deadline and deadline!="Unknown":
                message+=f"Last date to apply is {deadline}. "

        message+="You will receive the application links by SMS shortly."

    twiml=f"""
<Response>
<Say voice="Polly.Joanna">{message}</Say>
</Response>
"""

    return {

        "statusCode":200,

        "headers":{"Content-Type":"text/xml"},

        "body":twiml

    }