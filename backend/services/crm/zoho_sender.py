import requests
from utils.logger import logger
from database.models import EmailDraft
from sqlalchemy.orm import Session

ZOHO_SENDMAIL_URL = "https://www.zohoapis.com/crm/v2.1/Emails/send"
ZOHO_NOTES_URL = "https://www.zohoapis.com/crm/v2.1/Notes"
ZOHO_ACCESS_TOKEN = "1000.e1588bfbcda09df374eb6594a5af895f.aa07b8175386156f94cbcc6be441f4da"   # Replace with environment variable later


def send_email_to_zoho(db: Session, email_id: str):
    """
    Fetch email draft from DB and send to Zoho CRM via API.
    """

    # 1. Fetch Email from DB
    email_row = db.query(EmailDraft).filter(EmailDraft.email_id == email_id).first()
    if not email_row:
        raise Exception("Email not found in database")

    logger.info("Email fetched successfully from DB")

    # -----------------------------
    # 2. Prepare Zoho CRM Payload
    # -----------------------------
    payload = {
        "from": {"email": "sunil@saturam.com"},          # Replace
        "to": [{"email": email_row.to_email}],
        "subject": email_row.subject,
        "content": email_row.body_text
    }

    # -----------------------------
    # 3. Send Email to Zoho CRM API
    # -----------------------------
    headers = {
        "Authorization": f"Zoho-oauthtoken {ZOHO_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(ZOHO_SENDMAIL_URL, json=payload, headers=headers)

    logger.info(f"Zoho API Response: {response.text}")

    # Optional: Also store email as CRM note
    save_as_crm_note(email_row, headers)

    return response.json()


def save_as_crm_note(email_row, headers):
    note_payload = {
        "data": [
            {
                "Note_Title": email_row.subject,
                "Note_Content": email_row.body_text,
                "Parent_Id": email_row.crm_contact_id,   # Must map in your DB
                "se_module": "Contacts"
            }
        ]
    }

    response = requests.post(ZOHO_NOTES_URL, json=note_payload, headers=headers)
    logger.info(f"Zoho Note Saved: {response.text}")
