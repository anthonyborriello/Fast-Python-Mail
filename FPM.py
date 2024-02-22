"""
Fast Python Mail is a simple Python script for sending emails with attachments quickly and easily. It can be used in your non-commercial projects.
Place this file in the folder where you need to send emails from.

Author: 🇮🇹   Antonio Borriello - https://antonioboriello.wordpress.com

This script is distributed under the MIT License. Feel free to use, modify, and distribute this script according to the terms of the MIT License. See the LICENSE file for more details.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(recipient, subject, body, attachments):
    # Configure SMTP server details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_username = 'your mail address'
    smtp_password = 'your password'

    # Create message object
    msg = MIMEMultipart()
    nickname = "Fast Python Mail"
    msg['From'] = f"{nickname} <{smtp_username}>"
    msg['To'] = recipient
    msg['Subject'] = subject

    # Add message body
    msg.attach(MIMEText(body, 'plain'))

    # Attach files if any
    for attachment in attachments:
        with open(attachment, "rb") as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment)}")
        msg.attach(part)

    # Connect and send email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, recipient, msg.as_string())

# Request user information
recipient = input("Enter the recipient's email address: ")
subject = input("Enter the email subject: ")
body = input("Enter the email body: ")

# Ask if the user wants to attach files
attach_files = input("Do you want to attach any file? (yes/no): ").lower()

if attach_files in ['yes', 'y']:
    # Get only visible files in the current directory
    visible_files = [file for file in os.listdir() if not file.startswith('.')]

    # Show visible files
    print("Files available in the folder:")
    for i, file in enumerate(visible_files, 1):
        print(f"{i}. {file}")

    # Ask user to input numbers of files to attach
    file_numbers_input = input("Enter the numbers of files to attach separated by spaces, or enter 'all' for everything: ")
    file_numbers = file_numbers_input.split()

    # Initialize list of attachments
    attachments = []

    # Select files to attach
    if 'all' in file_numbers:
        attachments = visible_files
    else:
        for number in file_numbers:
            try:
                file_number = int(number)
                if 1 <= file_number <= len(visible_files):
                    attachments.append(visible_files[file_number - 1])
                else:
                    print(f"The number {file_number} is invalid.")
            except ValueError:
                print(f"The value {number} is not a valid number.")

    # Send the email
    send_email(recipient, subject, body, attachments)
    print("Email sent successfully!")
elif attach_files in ['no', 'n']:
    # Send the email without attachments
    send_email(recipient, subject, body, [])
    print("Email sent successfully!")
else:
    print("Invalid input. Please respond with 'yes' or 'no'.")
