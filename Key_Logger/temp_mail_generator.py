import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

class EmailSender:

    def __init__(self, sender_email= "testing.purposes1989@gmail.com", app_password= "ypcm vlyj zhok vuhl", smtp_server="smtp.gmail.com", smtp_port=465):
        self.sender_email = sender_email
        self.app_password = app_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def prepare_email(self, receiver_email, subject, body, attachments= None):
        #  Create the message object and set up headers
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        #  Attach the body of the email
        message.attach(MIMEText(body, 'plain'))

        # Add Attachments if provided
        if attachments:
            for attachment in attachments:
                self.add_attachment(message, attachment)
        
        return message

    def add_attachment(self, message, attachment_path):
        if os.path.isfile(attachment_path):
            filename = os.path.basename(attachment_path)
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octect-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                message.attach(part)
        else:
            print(f"Attachment {attachment_path} not found !")
    
    def send_email(self, receiver_email, subject, body, attachments = None):
         # Prepare the email message
        message = self.prepare_email(receiver_email, subject, body, attachments)
        
        # Sending the email
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, receiver_email, message.as_string())
                print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

# Example of using the class to send an email with or without attachments
# if __name__ == "__main__":

#     email_sender = EmailSender()
#     receiver_email = "testing.purposes1989@gmail.com"
#     subject = "Subject: Here is your attachment"
#     body = "Hello, this is the body of the email. Please find the attached file."
#     attachments = ["./Test-Logo.svg.png"]  # List of attachment paths

#     # Call the method to send an email with attachments
#     email_sender.send_email(receiver_email, subject, body, attachments)



