"""
Forwards articles matching keyword triggers immediately.
"""
import re
import logging
from typing import List, Dict, Any
from .gmail_client import GmailClient
from .config import Config

logger = logging.getLogger(__name__)


class Trigger:
    def __init__(self, config: Config) -> None:
        self.rules = config.triggers
        self.gmail = GmailClient(creds_path='token.json', config=config)

    def run(self, items: List[Dict[str, Any]]) -> None:
        for art in items:
            for rule in self.rules:
                if re.search(rule.keyword, art['summary'], re.IGNORECASE):
                    try:
                        self.gmail.send_html(
                            to=rule.email,
                            subject=f"Trigger: {rule.keyword}",
                            html=art['summary']
                        )
                        logger.info("Triggered forward for %s", rule.keyword)
                    except Exception:
                        logger.exception("Failed to forward triggered summary")