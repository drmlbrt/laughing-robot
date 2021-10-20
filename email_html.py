import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tqdm import tqdm
from time import sleep
import random






def myname():
    namelist= ["bart", "mattis", "maxim", "charlotte", "tipsie"]
    while True:
        for i in tqdm(namelist, desc="Progress Bar"):

            sleep(0.5)
        return

myname()



def email():
    sender_email = "ZTP-DCN-WORKGROUPSWITCH@mil.intra"
    receiver_email = "CCVC-N-TECHBU-DCN@mil.be"
    port = 25
    smtp_server = "10.8.145.37"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Zero Touch Provisioning"
    message["From"] = sender_email
    message["To"] = receiver_email
    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    This is an automatic text email directly from the switch"""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           This is an automatic email from the switch?<br>
        </p>
      </body>
    </html>
    """
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    # Create secure connection with server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.sendmail(sender_email, receiver_email, message.as_string())

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server = smtplib.SMTP(smtp_server, port)
        server.quit()
    return

