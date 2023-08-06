import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import shutil

def get_files_in_folders(folder_paths):
    file_paths = []
    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
    return file_paths

def get_filenames_in_folders(folder_paths):
    file_names = []
    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_names.append(file_name)
    return file_names


def send(recipients,subject,message, folder_paths):
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

    # Get all file paths in the folders
    attachment_paths = get_files_in_folders(folder_paths)

    # Get all file names in the folders
    attachment_file_names = get_filenames_in_folders(folder_paths)

    # Add the email body with the list of attached files
    message += "\n\r".join(attachment_file_names)
    msg.attach(MIMEText(message, 'plain'))

    # Find files with the specified extension in the folder
    # attachment_paths = []
    # sendEmail = 0
    # for file_name in os.listdir(folder_path):
    #     if file_name.endswith(file_extension):
    #         attachment_paths.append(os.path.join(folder_path, file_name))
    #         sendEmail = 1
    # if sendEmail==0:
    #     return 0

    # Attach the files to the email
    for file_path in attachment_paths:
        attachment = MIMEBase("application", "octet-stream")
        with open(file_path, "rb") as file:
            attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(file_path)}",
        )
        msg.attach(attachment)
        # use the shutil.move() function to move the file
        if os.path.exists('./backup/'+os.path.basename(file_path)):
            os.replace('./backup/'+os.path.basename(file_path), os.path.basename(file_path))
        shutil.move(file_path, './backup/')

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
