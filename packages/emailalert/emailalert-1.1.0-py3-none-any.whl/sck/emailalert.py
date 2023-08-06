import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send(recipients,subject,message, folder_path, file_extension):
    # Email details
    smtp_server = 'mrelay.noc.sony.co.jp'
    smtp_port = 25
    sender = 'SCK-H5BAREVOS-NGK-SYSADMIN@sony.com'

    # Create a MIME text object
    #msg = MIMEText(message)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    #msg['To'] = recipient
    msg['To'] = ', '.join(recipients)

    msg.attach(MIMEText(message, 'plain'))

    # Attach the file
    # with open(attachment, 'rb') as attachement:
    #     part = MIMEBase('application', 'octet-stream')
    #     part.set_payload(attachement.read())
    #     encoders.endoe_base64(part)
    #     part.add_header('Content-Disposition', f'attachement; filename={attachement}')

    #     msg.attach(part)

    # Find files with the specified extension in the folder
    attachment_paths = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(file_extension):
            attachment_paths.append(os.path.join(folder_path, file_name))

    # Attach multiple files
    for attachment_path in attachment_paths:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')

            msg.attach(part)

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        try:    
            server.sendmail(sender, recipients, msg.as_string())

            return 1
        except Exception as e:
            print('An error occurred:', str(e))
            return 0
        finally:
            # Disconnect from the SMTP server
            server.quit()
