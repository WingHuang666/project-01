import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from config import (
    NEWSAPI_KEY, NEWS_SOURCES, TIME_CONFIG, 
    ARTICLE_FILTERS, PRIORITY_TOPICS, CATEGORIES
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsFetcher:
    """Fetch news from multiple sources"""
    
    def __init__(self):
        self.articles = []
        self.session = requests.Session()
        self.session.timeout = 10
        
    def fetch_from_newsapi(self) -> List[Dict]:
        """Fetch articles from NewsAPI"""
        if not NEWSAPI_KEY or not NEWS_SOURCES['newsapi']['enabled']:
            logger.warning('NewsAPI key not configured or disabled')
            return []
        
        articles = []
        base_url = 'https://newsapi.org/v2/everything'
        
        # Calculate date from which to fetch
        look_back_hours = TIME_CONFIG.get('look_back_hours', 24)
        from_date = datetime.utcnow() - timedelta(hours=look_back_hours)
        from_date_str = from_date.strftime('%Y-%m-%d')
        
        for endpoint in NEWS_SOURCES['newsapi']['endpoints']:
            try:
                params = {
                    'q': endpoint['query'],
                    'language': endpoint['language'],
                    'sortBy': endpoint['sort_by'],
                    'from': from_date_str,
                    'apiKey': NEWSAPI_KEY,
                    'pageSize': 50
                }
                
                logger.info(f"Fetching from NewsAPI: {endpoint['name']}")
                response = self.session.get(base_url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if data.get('status') == 'ok':
                    for article in data.get('articles', []):
                        processed = self._process_newsapi_article(
                            article, 
                            endpoint['category']
                        )
                        if processed:
                            articles.append(processed)
                            
            except Exception as e:
                logger.error(f"Error fetching from NewsAPI ({endpoint['name']}): {str(e)}")
                continue
        
        logger.info(f"Fetched {len(articles)} articles from NewsAPI")
        return articles
    
    def fetch_from_rss(self) -> List[Dict]:
        """Fetch articles from RSS feeds"""
        if not NEWS_SOURCES['rss']['enabled']:
            logger.warning('RSS feeds disabled')
            return []
        
        articles = []
        
        for source in NEWS_SOURCES['rss']['sources']:
            try:
                logger.info(f"Fetching from RSS: {source['name']}")
                feed = feedparser.parse(source['url'])
                
                if feed.get('entries'):
                    for entry in feed['entries'][:20]:  # Limit to 20 per source
                        processed = self._process_rss_article(
                            entry, 
                            source['category'],
                            source['name']
                        )
                        if processed:
                            articles.append(processed)
                            
            except Exception as e:
                logger.error(f"Error fetching from RSS ({source['name']}): {str(e)}")
                continue
        
        logger.info(f"Fetched {len(articles)} articles from RSS")
        return articles
    
    def _process_newsapi_article(self, article: Dict, category: str) -> Optional[Dict]:
        """Process and validate NewsAPI article"""
        try:
            # Check required fields
            if not all([article.get('title'), article.get('description'), article.get('url')]):
                return None
            
            # Skip if published date is too old
            if article.get('publishedAt'):
                pub_date = datetime.fromisoformat(
                    article['publishedAt'].replace('Z', '+00:00')
                )
                hours_old = (datetime.now(pub_date.tzinfo) - pub_date).total_seconds() / 3600
                if hours_old > TIME_CONFIG.get('look_back_hours', 24):
                    return None
            
            # Filter by word count
            description = article.get('description', '')
            if len(description.split()) < ARTICLE_FILTERS['min_word_count']:
                return None
            
            # Check for excluded keywords
            full_text = f"{article['title']} {description}".lower()
            for keyword in ARTICLE_FILTERS['exclude_keywords']:
                if keyword.lower() in full_text:
                    return None
            
            return {
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'source': article.get('source', {}).get('name', 'Unknown'),
                'image': article.get('urlToImage'),
                'published_at': article.get('publishedAt'),
                'category': category,
                'provider': 'NewsAPI',
                'content': article.get('content', '')
            }
            
        except Exception as e:
            logger.debug(f"Error processing NewsAPI article: {str(e)}")
            return None
    
    def _process_rss_article(self, entry: Dict, category: str, source_name: str) -> Optional[Dict]:
        """Process and validate RSS article"""
        try:
            title = entry.get('title', '')
            description = entry.get('summary', '') or entry.get('description', '')
            url = entry.get('link', '')
            
            # Check required fields
            if not all([title, description, url]):
                return None
            
            # Filter by word count
            if len(description.split()) < ARTICLE_FILTERS['min_word_count']:
                return None
            
            # Check for excluded keywords
            full_text = f"{title} {description}".lower()
            for keyword in ARTICLE_FILTERS['exclude_keywords']:
                if keyword.lower() in full_text:
                    return None
            
            # Get published date
            pub_date = None
            if entry.get('published'):
                try:
                    pub_date = entry['published']
                except:
                    pass
            
            return {
                'title': title,
                'description': description,
                'url': url,
                'source': source_name,
                'image': None,
                'published_at': pub_date,
                'category': category,
                'provider': 'RSS',
                'content': description
            }
            
        except Exception as e:
            logger.debug(f"Error processing RSS article: {str(e)}")
            return None
    
    def fetch_all(self) -> List[Dict]:
        """Fetch from all sources"""
        logger.info("Starting to fetch news from all sources...")
        
        articles = []
        articles.extend(self.fetch_from_newsapi())
        articles.extend(self.fetch_from_rss())
        
        # Remove duplicates based on title
        unique_articles = []
        seen_titles = set()
        
        for article in articles:
            title_lower = article['title'].lower()
            if title_lower not in seen_titles:
                unique_articles.append(article)
                seen_titles.add(title_lower)
        
        logger.info(f"Total unique articles fetched: {len(unique_articles)}")
        self.articles = unique_articles
        return unique_articles
    
    def calculate_priority_score(self, article: Dict) -> int:
        """Calculate priority score for article based on content and topics"""
        score = 0
        
        full_text = f"{article['title']} {article['description']}".lower()
        
        # Check for priority topics
        for topic, weight in PRIORITY_TOPICS.items():
            if topic.lower() in full_text:
                score += weight
        
        # Category bonus
        if article['category'] in ['Artificial Intelligence', 'Technology']:
            score += 3
        elif article['category'] in ['Business & Economy']:
            score += 2
        
        return score
    
    def rank_articles(self, articles: Optional[List[Dict]] = None) -> List[Dict]:
        """Rank articles by priority score"""
        if articles is None:
            articles = self.articles
        
        # Add priority score to each article
        for article in articles:
            article['priority_score'] = self.calculate_priority_score(article)
        
        # Sort by priority score (descending)
        ranked = sorted(articles, key=lambda x: x['priority_score'], reverse=True)
        
        logger.info(f"Articles ranked. Top article score: {ranked[0]['priority_score'] if ranked else 0}")
        return ranked
