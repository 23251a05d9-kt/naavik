# Naavik – Voice-first Opportunity Discovery System

## Problem

Government opportunities such as exams, scholarships, and jobs are scattered across many portals. Users must constantly search for updates and often miss opportunities because they are unaware of them in time.

## Solution

Naavik is a voice-first system that proactively informs users about opportunities they are eligible for through automated phone calls.

Instead of searching for opportunities, users simply receive notifications when relevant opportunities appear.

---

## Key Features

- AI extraction of government notification PDFs
- Automatic eligibility matching
- Voice-based interaction using phone calls
- Serverless architecture using AWS
- Opportunity announcements via IVR

---

## Technology Stack

AWS Lambda – backend logic  
Amazon S3 – PDF storage and static website hosting  
Amazon DynamoDB – opportunity database  
Amazon Bedrock – AI extraction of opportunity data  
Twilio Voice API – automated phone calls and IVR  
PyPDF2 – PDF text extraction  
HTML + JavaScript – web interface

---

## Architecture Overview

Opportunity Processing Pipeline:

Government Notification PDF  
→ Amazon S3  
→ AWS Lambda  
→ PyPDF2  
→ Amazon Bedrock  
→ DynamoDB

User Interaction Pipeline:

Website  
→ AWS Lambda API  
→ Twilio Voice  
→ IVR Interaction  
→ Eligibility Engine  
→ DynamoDB  
→ Voice Response

---

## Demo Flow

1. Upload government notification PDF
2. AI extracts opportunity data
3. Data stored in DynamoDB
4. User enters phone number on website
5. System calls the user
6. IVR collects user input
7. System announces eligible opportunities

---

## Future Improvements

- Multi-language voice support
- SMS notification with application links
- Expanded opportunity coverage (scholarships, training programs)

---

## Project Vision

Naavik aims to bridge the information gap between opportunities and people who need them, especially in rural areas and among users with limited digital literacy.