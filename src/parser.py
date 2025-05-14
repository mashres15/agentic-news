"""
Parses raw Gmail messages into structured articles.
"""
import base64
import logging
from newspaper import Article
from typing import Dict, Any

logger = logging.getLogger(__name__)


class Parser:
    @staticmethod
    def extract(msg: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts title, body, and published date from a Gmail message payload.
        """
        parts = msg.get('payload', {}).get('parts', [])
        raw_html = ''
        raw_text = ''
        for p in parts:
            mime = p.get('mimeType')
            data = p.get('body', {}).get('data')
            if not data:
                continue
            content = base64.urlsafe_b64decode(data).decode('utf-8')
            if mime == 'text/html':
                raw_html = content
                break
            elif mime == 'text/plain':
                raw_text = content
        html = raw_html or raw_text
        article = Article('')
        article.set_html(html)
        try:
            article.parse()
            article.nlp()
        except Exception:
            logger.exception("Failed to parse article content")
        return {
            'id': msg.get('id'),
            'title': article.title or '',
            'body': article.text or raw_text,
            'published': int(msg.get('internalDate', 0))
        }