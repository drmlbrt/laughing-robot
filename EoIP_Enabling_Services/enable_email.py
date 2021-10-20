import cli
import time
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

file_server = '10.15.255.52'
smtp_server = "10.8.145.37"
cfgfile = "baseline.cfg"
eoipfile= "eoip.py"
tarfile= "Tcl.tar"
destination = 'running-config'
destinationflash = "flash:"
ios = "cat9k_iosxe.17.03.03.SPA.bin"


def email():
    sender_email = "ZTP-DCN-WORKGROUPSWITCH@mil.intra"
    receiver_email = "CCVC-N-TECHBU-DCN@mil.be"
    port = 25
    device_facts = json.dumps(get_facts())
    json_facts = json.loads(device_facts)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Zero Touch Provisioning - %s" %(json_facts["Hostname"])
    message["From"] = sender_email
    message["To"] = receiver_email
    # Create the plain-text and HTML version of your message
    text = ("""\
            Hi,
            This is an auto generated email from a ZTP-Enabled Switch:
            Device Facts:
            %s
            [TextFormatted]
            """%(device_facts))
    html = ("""\
            <html>
              <body>
                <p>Hi,<br>
                   This is an auto generated email from a ZTP-Enabled Switch<br>
                   <pre><code class="prettyprint">%s</code></pre>
                </p>
              </body>
            </html>
            """ %(device_facts))
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
        server.ehlo()  # Can be omitted
        # server.starttls(context=context) # Secure the connection
        server.ehlo()  # Can be omitted
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    return