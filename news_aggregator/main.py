#!/usr/bin/env python3
"""
Daily Tech News Aggregator
Fetches news from multiple sources and sends a daily digest email
"""

import logging
import sys
from datetime import datetime
from news_fetcher import NewsFetcher
from email_sender import EmailSender
from config import EMAIL_CONFIG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point"""
    try:
        logger.info("=" * 60)
        logger.info("Starting Daily Tech News Aggregator")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        # Fetch news
        logger.info("\n📰 Fetching news from all sources...")
        fetcher = NewsFetcher()
        articles = fetcher.fetch_all()
        
        if not articles:
            logger.error("No articles fetched from any source")
            return False
        
        logger.info(f"Total articles fetched: {len(articles)}")
        
        # Rank articles
        logger.info("\n🎯 Ranking articles by priority...")
        ranked_articles = fetcher.rank_articles(articles)
        
        # Log top articles
        logger.info("\nTop 10 Articles:")
        logger.info("-" * 60)
        for idx, article in enumerate(ranked_articles[:10], 1):
            logger.info(f"{idx}. [{article['category']}] {article['title']}")
            logger.info(f"   Source: {article['source']}")
            logger.info(f"   Priority Score: {article['priority_score']}")
            logger.info("-" * 60)
        
        # Select top articles for digest
        max_articles = EMAIL_CONFIG.get('max_articles', 10)
        digest_articles = ranked_articles[:max_articles]
        
        # Send email
        logger.info(f"\n📧 Sending email digest to {EMAIL_CONFIG['recipient_email']}...")
        sender = EmailSender(
            recipient_email=EMAIL_CONFIG['recipient_email']
        )
        
        success = sender.send_digest(digest_articles)
        
        if success:
            logger.info("✅ Email sent successfully!")
            logger.info("=" * 60)
            return True
        else:
            logger.error("❌ Failed to send email")
            logger.info("=" * 60)
            return False
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
