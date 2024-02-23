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

1. **Clone the repository:**
    ```bash
    sudo apt install git
    ```
    ```bash
    git clone https://github.com/anthonyborriello/Fast-Python-Mail.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd Fast-Python-Mail
    ```

4. **Run the script:**
    ```bash
    python fpmail.py
    ```
**Nickname selection:**

You have the option to skip selecting a nickname.<br>If left blank, the recipient will see your email address instead of a nickname in the email header.

**To select multiple files for attachments:**

When prompted, enter "yes" or "y" to attach files.
You will be prompted to navigate through the system's folders starting from the home directory.
Use the numbers provided to select folders or files.
To select multiple files, you can enter numbers separated by spaces (e.g., "1 3 5").
To select a range of files, you can use hyphens (e.g., "1-3" selects files 1, 2, and 3).
Once you've selected all desired files, press Enter to proceed.

**Common SMTP Servers:**

Gmail: smtp.gmail.com Port: 465
Hotmail: pod51000.outlook.com 587
Yahoo: smtp.mail.yahoo.com 465

## Author

🇮🇹   Antonio Borriello - [Website](https://antonioborriello.wordpress.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
