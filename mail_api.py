from fastapi import FastAPI
from imaplib import IMAP4_SSL
from email import message_from_bytes
from email.message import Message
from config import EMAIL, PASSWORD, IMAP_SERVER

app = FastAPI()

def extract_text_from_email(msg: Message):
    """Načíta len čistý text z e-mailu (bez HTML)"""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode(errors="ignore")
    else:
        return msg.get_payload(decode=True).decode(errors="ignore")
    return ""

def get_filtered_emails():
    with IMAP4_SSL(IMAP_SERVER) as mail:
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        status, data = mail.search(None, '(FROM "mosko@smartacoustic.sk")')
        ids = data[0].split()
        result = []

        for email_id in ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = message_from_bytes(raw_email)

            subject = msg["Subject"] or ""
            if "report" in subject.lower():
                body = extract_text_from_email(msg)
                result.append({
                    "subject": subject,
                    "from": msg["From"],
                    "date": msg["Date"],
                    "body": body.strip()
                })

        return result

@app.get("/maily")
def get_emails():
    return get_filtered_emails()
