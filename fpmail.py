"""
Fast Python Mail is a simple Python script for sending emails with attachments quickly and easily. It can be used in your non-commercial projects.

Author: 🇮🇹   Antonio Borriello - https://antonioboriello.wordpress.com

This script is distributed under the MIT License. Feel free to use, modify, and distribute this script according to the terms of the MIT License. See the LICENSE file for more details.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import re

CONFIG_FILE = 'config.json'

def create_config():
    config = {
        'username': '',
        'password': '',
        'nickname': ''
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def read_config():
    if not os.path.exists(CONFIG_FILE) or os.path.getsize(CONFIG_FILE) == 0:
        print("Configuration file not found or empty. Creating a new one...")
        create_config()

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def is_valid_email(email):
    # Pattern per l'indirizzo email
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    # Verifica se l'indirizzo email corrisponde al pattern
    if re.match(pattern, email):
        return True
    else:
        return False

def send_email(nickname, recipient, subject, body, attachments):
    config = read_config()
    smtp_server = config.get('smtp_server', '')
    smtp_port = config.get('smtp_port', 465)
    username = config['username']
    password = config['password']

    msg = create_message(nickname, username, recipient, subject, body, attachments)

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(username, password)
        server.sendmail(username, recipient, msg.as_string())

def create_message(nickname, sender, recipient, subject, body, attachments):
    msg = MIMEMultipart()
    msg['From'] = f"{nickname} <{sender}>"
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for attachment in attachments:
        with open(attachment, "rb") as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment)}")
        msg.attach(part)

    return msg

def navigate_folders(current_path):
    RESET = '\033[0m'
    FOLDER_COLOR = '\033[94m'  # Folders are colored

    while True:
        print("\nCurrent path:", current_path)
        print("Folders and files available in the current directory:")
        entries = os.listdir(current_path)
        for i, entry in enumerate(entries, 1):
            full_path = os.path.join(current_path, entry)
            if os.path.isdir(full_path):
                print(f"{i}. {FOLDER_COLOR}[Folder] {entry}{RESET}")
            else:
                print(f"{i}. [File] {entry}")
        print("0. Go back")
        choice = input("Enter the number of the folder or file to enter or 0 to go back: ")
        if choice == '0':
            if current_path != os.path.expanduser("~"):
                current_path = os.path.dirname(current_path)
            else:
                print("Cannot go back from the home directory.")
        elif choice.isdigit() and 0 < int(choice) <= len(entries):
            selected_entry = entries[int(choice) - 1]
            full_path = os.path.join(current_path, selected_entry)
            if os.path.isdir(full_path):
                current_path = full_path
            else:
                return [full_path]  # Return a list with the selected file path
        else:
            file_selections = choice.split()
            selected_files = []
            for selection in file_selections:
                if '-' in selection:
                    start, end = map(int, selection.split('-'))
                    selected_files.extend(entries[start-1:end])
                elif selection.isdigit() and 0 < int(selection) <= len(entries):
                    selected_files.append(entries[int(selection) - 1])
                else:
                    print(f"Invalid selection: {selection}")
            selected_paths = [os.path.join(current_path, entry) for entry in selected_files]
            return selected_paths

def main():
    config = read_config()

    if not config['username'] or not config['password']:
        print("Let's add a new address!")
        config['username'] = input("Enter your email: ")
        config['password'] = input("Enter your password: ")
        save_config(config)

    if not config['nickname']:
        config['nickname'] = input("Enter your nickname for the sender's name (case sensitive): ")
        save_config(config)

    recipient = input("Enter the recipient's email address: ")
    while not is_valid_email(recipient):
        print("Invalid email address. Please enter a valid email address.")
        recipient = input("Enter the recipient's email address: ")

    subject = input("Enter the email subject: ")
    body = input("Enter the email body: ")

    # Check if the user's email provider is not Gmail
    if not config['username'].endswith('@gmail.com') and (not config.get('smtp_server') or not config.get('smtp_port')):
        print("Your provider is not Gmail.")
        smtp_server = input("Enter your SMTP server address: ")
        smtp_port = input("Enter your SMTP port: ")
        config['smtp_server'] = smtp_server
        config['smtp_port'] = smtp_port
        save_config(config)

    attach_files = input("Do you want to attach any file? (yes/no): ").lower()

    attachments = []

    if attach_files in ['yes', 'y']:
        root_path = os.path.expanduser("~")  # Home directory
        selected_files = navigate_folders(root_path)
        attachments.extend(selected_files)

    if attachments or attach_files in ['no', 'n']:
        send_email(config['nickname'], recipient, subject, body, attachments)
        print("Email sent successfully!")
    else:
        send_email(config['nickname'], recipient, subject, body, [])
        print("Email sent successfully without attachments!")

if __name__ == "__main__":
    main()
