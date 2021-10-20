import smtplib

port = 25  # For SSL
smtp_server = "10.8.145.37"
sender_email = "ZTP-DCN-WORKGROUPSWITCH@mil.intra"
receiver_email = "CCVC-N-TECHBU-DCN@mil.be"
#context = ssl.create_default_context()
message = "TestBart"

try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo() # Can be omitted
    #server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.sendmail(sender_email, receiver_email, message)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()