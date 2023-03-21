from __future__ import print_function
import base64

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.message import EmailMessage

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from datetime import datetime
from campaigns.models import Customer, EmailTemplate, Emails
from django.contrib import messages


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def send_emails_to_users(request, selected_template_id):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    print("sending emails to users")

    list_of_customers =  list(Customer.objects.all())
    selected_template = EmailTemplate.objects.get(id=selected_template_id)
    title = EmailTemplate.objects.get(id=selected_template_id).subject
    body = EmailTemplate.objects.get(id=selected_template_id).body
    

 
    sent_messages=[] 
    list_of_valid_customers = []
    for customer in list_of_customers:
        try:
            service = build('gmail', 'v1', credentials=creds)

            message = EmailMessage()

            message.set_content(body)

            message['From'] = 'Marketing'
            message['Subject'] = title
            message['To'] =customer.email

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {
                'raw': encoded_message
            }

            msg = (service.users().messages().send
                    (userId="me", body=create_message).execute())
            print(str(msg))
            sent_messages.append(msg)
            print(F'Messages Id: {msg["id"]}')
            list_of_valid_customers.append(customer)
        except HttpError as error:
            print(F'An error occurred: {error}')
            print (f"Email not sent to {customer.email}")
            
    messages.success(request, "Emails sent!." )

    update_DB_with_sent_emails(selected_template, request.user, list_of_valid_customers)
        
    return sent_messages

def update_DB_with_sent_emails(selected_template, user, list_of_customers):
    date_sent = datetime.now()
    for customer in list_of_customers:
        Emails.objects.create(
            email_address=customer,
            email_template=selected_template,
            date_sent=date_sent,
            sent_by=user
        )
    print ("Emails saved to database")
    

    