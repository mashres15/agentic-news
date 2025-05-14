"""
Gmail client with fetch & send utilities.
"""
import base64
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Any
from .config import Config

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']


class GmailClient:
    def __init__(self, creds_path: str, config: Config) -> None:
        creds = Credentials.from_authorized_user_file(creds_path, SCOPES)
        self.service = build('gmail', 'v1', credentials=creds)
        self.config = config

    def fetch_unread(self) -> list[dict[str, Any]]:
        query = (
            f'is:unread after:{Config.__fields__["schedule_time"]} '
            f'from:({" OR ".join(self.config.sources)})'
        )
        logger.info(f"Fetching unread emails with query: %s", query)
        res = (self.service.users().messages()
                   .list(userId='me', q=query)
                   .execute())
        msgs = res.get('messages', [])
        return [self.service.users().messages()
                         .get(userId='me', id=m['id'], format='full')
                         .execute() for m in msgs]

    def send_html(self, to: str, subject: str, html: str) -> None:
        message = (f"From: me\r\n"
                   f"To: {to}\r\n"
                   f"Subject: {subject}\r\n"
                   f"Content-Type: text/html; charset=UTF-8\r\n\r\n"
                   f"{html}")
        raw = base64.urlsafe_b64encode(message.encode()).decode()
        self.service.users().messages().send(
            userId='me', body={'raw': raw}).execute()
        logger.info("Sent email to %s with subject '%s'", 