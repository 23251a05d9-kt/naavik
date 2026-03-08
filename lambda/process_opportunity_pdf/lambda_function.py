import json
import boto3
import io
import uuid
from PyPDF2 import PdfReader

# AWS clients
s3 = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")
dynamodb = boto3.resource("dynamodb")

# DynamoDB table
table = dynamodb.Table("naavik_opportunities")

# Bedrock inference profile
MODEL_ID = "arn:aws:bedrock:ap-south-1:205650278002:application-inference-profile/mmaq2a0payw8"


def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print("Processing file:", key)

    # Download PDF
    response = s3.get_object(Bucket=bucket, Key=key)
    pdf_bytes = response['Body'].read()

    # Extract text
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    print("Text extracted. Sending to Bedrock...")

    prompt = f"""
Extract structured information from this government job or exam notification.

Return ONLY raw JSON (no markdown, no code blocks).

Fields required:
opportunity_name
organization
min_age
max_age
qualification
application_deadline
vacancies

TEXT:
{text[:4000]}
"""

    body = json.dumps({
        "schemaVersion": "messages-v1",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": prompt}
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 500,
            "temperature": 0
        }
    })

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=body
    )

    result = json.loads(response["body"].read())

    print("Raw model response:", result)

    ai_output = result["output"]["message"]["content"][0]["text"]

    # Remove markdown if model still adds it
    ai_output = ai_output.replace("```json", "").replace("```", "").strip()

    print("Cleaned AI output:", ai_output)

    try:
        data = json.loads(ai_output)
    except:
        print("AI output could not be parsed, using fallback.")
        data = {
            "opportunity_name": "Unknown",
            "organization": "Unknown",
            "min_age": None,
            "max_age": None,
            "qualification": "Unknown",
            "application_deadline": "Unknown",
            "vacancies": None
        }

    opportunity_id = str(uuid.uuid4())

    table.put_item(
        Item={
            "opportunity_id": opportunity_id,
            "name": data.get("opportunity_name"),
            "organization": data.get("organization"),
            "min_age": data.get("min_age"),
            "max_age": data.get("max_age"),
            "qualification": data.get("qualification"),
            "deadline": data.get("application_deadline"),
            "vacancies": data.get("vacancies")
        }
    )

    print("Opportunity saved to DynamoDB")

    return {
        "statusCode": 200,
        "body": json.dumps("Opportunity processed successfully")
    }