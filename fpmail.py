"""
Fast Python Mail is a simple Python script for sending emails with attachments quickly and easily. It can be used in your non-commercial projects.

Author: 🇮🇹   Antonio Borriello - https://antonioboriello.wordpress.com

This script is distributed under the MIT License. Feel free to use, modify, and distribute this script according to the terms of the MIT License. See the LICENSE file for more details.
"""

import os
import smtplib
import json
import re
import requests
import xml.etree.ElementTree as ET
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

CONFIG_FILE = 'config.json'

def get_domain_from_email(email):
    match = re.match(r".*@(.+)$", email)
    if match:
        return match.group(1)
    else:
        print("Invalid email address.")
        return None

def get_smtp_info_autoconfig(email):
    domain = get_domain_from_email(email)
    if domain:
        url1 = f'https://autoconfig.thunderbird.net/v1.1/{domain}'
        url2 = f'http://autoconfig.{domain}/mail/config-v1.1.xml?emailaddress={email}'

        urls = [url1, url2]

        for url in urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return parse_xml(response.content)
            except Exception as e:
                print(f"An error occurred: {e}")
    
        print("Failed to fetch SMTP information.")
        return None

def parse_xml(xml_content):
    try:
        root = ET.fromstring(xml_content)
        smtp_servers = []
        for server in root.findall('.//outgoingServer'):
            hostname = server.find('hostname').text
            port = int(server.find('port').text)
            security = server.find('socketType').text
            smtp_servers.append({'hostname': hostname, 'port': port, 'security': security})
        return smtp_servers
    except Exception as e:
        print(f"An error occurred while parsing XML: {e}")
        return None

def create_config():
    config = {
        'smtp_server': "",
        'smtp_port': "",
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
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

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

def send_email(nickname, recipient, subject, body, attachments):
    config = read_config()
    sender = config['username']
    password = config['password']
    smtp_server = config['smtp_server']
    smtp_port = int(config['smtp_port'])

    msg = create_message(nickname, sender, recipient, subject, body, attachments)

    if smtp_port == 465:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    else:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

    server.login(sender, password)
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()

def navigate_folders(current_path):
    RESET = '\033[0m'
    FOLDER_COLOR = '\033[94m'

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
                return [full_path]
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
    print_logo()
    config = read_config()

    if not config['smtp_server'] or not config['smtp_port']:
        print("Let's add a new address!")
        while True:
            config['username'] = input("Enter your email: ")
            if is_valid_email(config['username']):
                break
            else:
                print("Invalid email address. Please enter a valid email address.")

        config['password'] = input("Enter your password: ")
        config['nickname'] = input("Enter your nickname for the sender's name (case sensitive): ")

        smtp_info = get_smtp_info_autoconfig(config['username'])
        if smtp_info:
            print("SMTP Information:")
            server = smtp_info[0]
            print(f"Hostname: {server['hostname']}, Port: {server['port']}, Security: {server['security']}")
            config['smtp_server'] = server['hostname']
            config['smtp_port'] = server['port']
            save_config(config)
        else:
            print("SMTP information not found. You need to provide SMTP details manually.")
            config['smtp_server'] = input("Enter your SMTP server address: ")
            config['smtp_port'] = input("Enter your SMTP port: ")
            save_config(config)

    recipient = input("Enter the recipient's email address: ")
    while not is_valid_email(recipient):
        print("Invalid email address. Please enter a valid email address.")
        recipient = input("Enter the recipient's email address: ")

    subject = input("Enter the email subject: ")
    body = input("Enter the email body: ")

    attach_files = input("Do you want to attach any file? (yes/no): ").lower()

    attachments = []

    if attach_files in ['yes', 'y']:
        root_path = os.path.expanduser("~")
        selected_files = navigate_folders(root_path)
        attachments.extend(selected_files)

    send_email(config['nickname'], recipient, subject, body, attachments)
    if attachments:
        print("Email sent successfully with attachments!")
    else:
        print("Email sent successfully without attachments!")

def print_logo():
    logo = """
   __                       _ _
  / _|                     (_) |
 | |_ _ __  _ __ ___   __ _ _| |
 |  _| '_ \| '_ ` _ \ / _` | | |
 | | | |_) | | | | | | (_| | | |
 |_| | .__/|_| |_| |_|\__,_|_|_|
     | |
     |_|
    \n"""
    print(logo)
    print("""Send messages with attachments quickly and easily""")

if __name__ == "__main__":
    main()
