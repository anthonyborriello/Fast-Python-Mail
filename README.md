# Fast Python Mail (fpmail)

Fast Python Mail (fpmail) is a simple Python script designed to swiftly send emails with attachments. It offers a hassle-free solution for sending emails and is well-suited for non-commercial projects, making it ideal for personal or small-scale use.

## Features

- Effortlessly sends emails with attachments.
- Simple and intuitive to use.
- Customizable to suit your specific requirements.
- Able to handle various providers.
- Automatically configures itself on first run, prompting the user to input necessary information, and creates a JSON file (`config.json`) to store all configurations.
- Allows selection of multiple files for sending attachments and enables navigation through the system's folders, starting from the home directory.

## Usage

1. **Download the Python file:**
    ```bash
   wget https://raw.githubusercontent.com/anthonyborriello/Fast-Python-Mail/main/fpmail.py
    ```
2. **Run the script:**
    ```bash
    python fpmail.py
    ```
**Nickname selection:**

You have the option to skip selecting a nickname.  
If left blank, the recipient will see your email address instead of a nickname in the email header.


**To select multiple files for attachments:**

When prompted, enter "yes" or "y" to attach files.
You will be prompted to navigate through the system's folders starting from the home directory.
Use the numbers provided to select folders or files.
To select multiple files, you can enter numbers separated by spaces (e.g., "1 3 5").
To select a range of files, you can use hyphens (e.g., "1-3" selects files 1, 2, and 3).
Once you've selected all desired files, press Enter to proceed.

**Common SMTP Servers:**

- Gmail: `smtp.gmail.com` Port: 465 (SSL)  
  *Requires an App Password for authentication.*
- Hotmail/Outlook: `smtp.office365.com` Port: 587 (STARTTLS)  
- Yahoo: `smtp.mail.yahoo.com` Port: 465 (SSL)  
  *Requires an App Password for authentication.*
- AOL: `smtp.aol.com` Port: 587 (STARTTLS)  
  *Requires an App Password for authentication.*
- iCloud: `smtp.mail.me.com` Port: 587 (STARTTLS)  
  *Requires an App Password for authentication.*

## Author

Antonio Borriello [antonioborriello.wordpress.com](https://antonioborriello.wordpress.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

![fpmail](https://github.com/user-attachments/assets/6c1ea1c3-4b3a-4b8d-8f50-6c2c04706a0c)


