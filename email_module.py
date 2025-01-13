# email_module.py for epitech students 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def send_excel_file(file_path, sender_name):
    """
    Sends the Excel file to jean1.noriot@epitech.eu
    """
    try:
        # Get sender's email
        sender_email = input("Enter your Epitech email (@epitech.digital): ")
        if not sender_email.endswith("@epitech.digital"):
            sender_email += "@epitech.digital"
        password = input("Enter your email password: ")

        # Create email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = "jean1.noriot@epitech.eu"
        msg['Subject'] = "Planning et reporting concernant"

        # Email body
        body = "Here is my updated excel file with my current submissions,\n\nCordially,"
        msg.attach(MIMEText(body, 'plain'))

        # Attach Excel 
        with open(file_path, 'rb') as f:
            excel_attachment = MIMEApplication(f.read(), _subtype='xlsx')
            excel_attachment.add_header('Content-Disposition', 'attachment', 
                                    filename=os.path.basename(file_path))
            msg.attach(excel_attachment)

        # Send 
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)

        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False