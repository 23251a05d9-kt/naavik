# Naavik – Voice-first Opportunity Discovery System

Naavik helps users discover government job and exam opportunities through automated voice calls.

Users enter their phone number on the website and receive a call where they can check eligibility for opportunities based on age, category, and education.

The system uses AI to extract information from government PDF notifications and automatically store them in a database.

## Technologies Used

AWS Lambda  
Amazon S3  
Amazon DynamoDB  
Amazon Bedrock  
Twilio Voice API  
PyPDF2  
HTML + JavaScript

## Architecture

PDF → S3 → Lambda → Bedrock → DynamoDB

User → Website → Lambda → Twilio Call → IVR → Eligibility Engine → DynamoDB