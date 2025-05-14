"""
Assembles and sends the daily digest email.
"""
import datetime
import logging
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader
from .gmail_client import GmailClient
from .config import Config

logger = logging.getLogger(__name__)


class Digest:
    def __init__(self, config: Config) -> None:
        self.config = config
        env = Environment(loader=FileSystemLoader('src/agentic_news'))
        self.template = env.get_template('digest_template.html')
        self.gmail = GmailClient(creds_path='token.json', config=config)

    def send(self, items: List[Dict[str, Any]]) -> None:
        html = self.template.render(items=items, now=datetime.datetime.now())
        try:
            self.gmail.send_html(
                to=self.config.delivery_email,
                subject=f"Daily News Digest - {datetime.datetime.now().date()}",
                html=html
            )
            logger.info("Sent daily digest with %d items", len(items))
        except Exception:
            logger.exception("Failed to send daily digest")