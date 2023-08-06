import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import shutil

def get_files_in_folders(folder_paths):
    file_paths = []
    file_names = []
    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
                file_names.append(file)
    return file_paths, file_names

def send(recipients,subject,message_header,message_footer, folder_paths):
    # Email details
    smtp_server = 'mrelay.noc.sony.co.jp'
    smtp_port = 25
    #sender = 'SCK-H5BAREVOS-NGK-SYSADMIN@sony.com'
    sender = 'VOS_MAP_SYSTEM@sony.com'

    # Create a MIME text object
    #msg = MIMEText(message)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    #msg['To'] = recipient
    msg['To'] = ', '.join(recipients)

    # Get all file paths in the folders
    attachment_paths,attachment_filename = get_files_in_folders(folder_paths)

    # Create the HTML table with CSS styles
    table_html = '''
    <style>
        table {
            border-collapse: collapse;
            width: 70%;
        }
        th {
            background-color: #f2f2f2;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            width: 300px;
            text-align: left;
        }        
        table tr:hover {
            background-color: #e6e6e6 !important;
        }
    </style>

    <table>
        <tr>
            <th>データ仕様</th>
            <th>エラー発生ファイル</th>
        </tr>
    '''
    for index, (file_name, file_path) in enumerate(zip(attachment_filename, attachment_paths)):
        spec = 'MCO'
        if 'VHS' in file_path:
            spec = 'LDD'
        elif 'TT' in file_path:
            spec = 'Tokyo'
        row_color = "#d1ffd4" if index % 2 != 0 else "#ffffff"
        table_html += f'<tr style="background-color: {row_color};" onmouseover="this.style.backgroundColor=\'#e6e6e6\';" onmouseout="this.style.backgroundColor=\'{row_color}\';">'
        table_html += f'<td style="width:30px;font-weight:bold">{spec}</td><td style="font-weight:bold">{file_name}</td></tr>'
        

    table_html += '</table>'

    # Create the email body as HTML
    message = message_header
    message += f'<html><body>{table_html}</body></html>'
    message += message_footer

    # Attach the email body
    msg.attach(MIMEText(message, 'html'))


    # Attach the files to the email
    # for file_path in attachment_paths:
    #     attachment = MIMEBase("application", "octet-stream")
    #     with open(file_path, "rb") as file:
    #         attachment.set_payload(file.read())
    #     encoders.encode_base64(attachment)
    #     attachment.add_header(
    #         "Content-Disposition",
    #         f"attachment; filename= {os.path.basename(file_path)}",
    #     )
    #     msg.attach(attachment)
    #     # Move the attached file to the backup folder
    #     backup_folder = backup_folders[0]
    #     if 'Tokyo' in file_path:
    #         backup_folder = backup_folders[1]  # Relative path to the backup folder
    #     elif 'MCO' in file_path:
    #         backup_folder = backup_folders[2]  # Relative path to the backup folder
    #     current_dir = os.getcwd()  # Get the current working directory
    #     backup_file_path = os.path.abspath(os.path.join(current_dir, backup_folder, os.path.basename(file_path)))
    #     shutil.move(file_path, backup_file_path)


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
