import smtplib
from email.mime.text import MIMEText

def send(recipients,subject,message):
    # Email details
    smtp_server = 'mrelay.noc.sony.co.jp'
    smtp_port = 25
    sender = 'SCK-H5BAREVOS-NGK-SYSADMIN@sony.com'

    # Create a MIME text object
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    #msg['To'] = recipient
    msg['To'] = ', '.join(recipients)

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)

        # Send the email
        server.sendmail(sender, recipients, msg.as_string())

        return 1
    except Exception as e:
        print('An error occurred:', str(e))
        return 0
    finally:
        # Disconnect from the SMTP server
        server.quit()
