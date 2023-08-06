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


def send(recipients,subject,message, folder_paths, backup_folders):
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
    #message += "\n\r".join(attachment_file_names)

    # Create the HTML table with CSS styles
    table_html = '''
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            border: 1px solid black;
            padding: 8px;
            width: 300px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }
    </style>

    <table>
        <tr>
            <th>エラーファイル</th>
        </tr>
    '''

    for filename in attachment_file_names:
        table_html += f'<tr><td>{filename}</td></tr>'

    table_html += '</table>'

    # Create the email body as HTML
    message += f'<html><body>{table_html}</body></html>'

    #msg.attach(MIMEText(message, 'plain'))

    # Attach the email body
    msg.attach(MIMEText(message, 'html'))

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
        # Move the attached file to the backup folder
        backup_folder = backup_folders[0]
        if 'Tokyo' in file_path:
            backup_folder = backup_folders[1]  # Relative path to the backup folder
        elif 'MCO' in file_path:
            backup_folder = backup_folders[2]  # Relative path to the backup folder
        current_dir = os.getcwd()  # Get the current working directory
        backup_file_path = os.path.abspath(os.path.join(current_dir, backup_folder, os.path.basename(file_path)))
        shutil.move(file_path, backup_file_path)

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
