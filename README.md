
# Assignment Submission Portal

**Student:** Ujala Adil  
**Registration Number:** FA23-BAI-045  
**Course:** DevOps for Cloud Computing (CSC418)

## Project Description
A Flask-based assignment submission portal with automated testing,
GitHub Actions CI, and automatic JSON test report delivery.

## Features
- Submit student name, registration number, assignment title, and URL
- Validate required fields and submission URLs
- Display saved submissions
- Run three automated tests
- Automatically deliver test results to a local receiver

## Installation
pip install -r requirements.txt

## Run Application
python app.py

Open http://127.0.0.1:5000

## Run Tests
python -m pytest -v

## Start Report Receiver
Set the REPORT_TOKEN environment variable, then run:

python receiver.py

The receiver listens at http://127.0.0.1:5001/report.

## CI Pipeline
GitHub Actions runs automated tests on every push.
Test reports are delivered through ngrok to the local receiver.
Configure RECEIVER_URL and REPORT_TOKEN as GitHub Actions secrets.
