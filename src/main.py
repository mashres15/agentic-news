"""
Entry point for the Agentic News Pipeline.
Schedules the pipeline and orchestrates all agents.
"""
import logging
import time
import schedule
from .config import load_config
from .gmail_client import GmailClient
from .parser import Parser
from .deduplicator import Deduplicator
from .summarizer import Summarizer
from .profiler import Profiler
from .ranker import Ranker
from .trigger import Trigger
from .digest import Digest


def main() -> None:
    # Initialize logging
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    # Load configuration
    config = load_config()
    gmail = GmailClient(creds_path='token.json', config=config)

    def run_pipeline() -> None:
        logger.info("Starting daily news pipeline run")
        # Fetch emails
        raw_messages = gmail.fetch_unread()
        # Parse content
        parsed = [Parser.extract(msg) for msg in raw_messages]
        # Deduplicate
        unique_articles = Deduplicator.dedupe(parsed)
        # Summarize
        for art in unique_articles:
            art['summary'] = Summarizer.summarize(art['body'])
        # Rank and profile
        ranked = Ranker.rank(unique_articles)
        # Trigger forwarding
        Trigger(config).run(ranked)
        # Send digest
        top_items = ranked[: config.daily_limit]
        Digest(config).send(top_items)
        # Mark as read
        ids = [msg['id'] for msg in raw_messages]
        gmail.service.users().messages().batchModify(
            userId='me',
            body={'ids': ids, 'removeLabelIds': ['UNREAD']}
        ).execute()
        logger.info("Pipeline run complete, marked %d emails as read", len(ids))

    # Schedule daily pipeline
    schedule.every().day.at(config.schedule_time).do(run_pipeline)
    logger.info("Scheduled pipeline at %s daily", config.schedule_time)

    # Keep process alive
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == '__main__':
    main()