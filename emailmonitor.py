import imaplib
import email 
from email.header import decode_header
import json

# Function to connect to Gmail and retrieve the latest email
def get_latest_email():
    # Set up your Gmail credentials
    username = "testimap.lama@gmail.com"
    password = "jrvt zmec nvbc yuwj"  # App password, not your Gmail password

    # Connect to the Gmail IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    
    # Select the mailbox you want to check
    mail.select("inbox")

    # Search for all emails in the inbox
    status, messages = mail.search(None, "ALL")

    # Convert messages to a list of email IDs
    email_ids = messages[0].split()

    # Fetch the most recent email
    latest_email_id = email_ids[-1]
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    
    # Parse the email content
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # If it's a bytes object, decode to a string
                subject = subject.decode(encoding if encoding else "utf-8")
            from_ = msg.get("From")
            
            # Initialize variables for the plain text and HTML parts
            plain_text = None
            html_text = None
            
            # If the email message is multipart
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    
                    # If it's plain text, extract it
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        try:
                            plain_text = part.get_payload(decode=True).decode()
                        except:
                            pass
                    elif content_type == "text/html" and "attachment" not in content_disposition:
                        try:
                            html_text = part.get_payload(decode=True).decode()
                        except:
                            pass

            else:
                # For non-multipart emails, get the payload directly
                content_type = msg.get_content_type()
                if content_type == "text/plain":
                    plain_text = msg.get_payload(decode=True).decode()
                elif content_type == "text/html":
                    html_text = msg.get_payload(decode=True).decode()

            # Return plain text if available, otherwise return HTML as fallback
            return f"{plain_text or html_text}"
                    # Prepare the JSON data
            # email_data = {
            #     "subject": subject,
            #     "from": from_,
            #     "body": plain_text or html_text
            # }
            
            # # Convert to JSON string
            # return json.dumps(email_data, indent=4)
    
    mail.logout()