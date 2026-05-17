# News Aggregator Configuration
import os

# API Keys (set these as GitHub Secrets)
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "huangwing666@gmail.com")

# News Sources
NEWS_SOURCES = {
    "newsapi": {
        "enabled": True,
        "api_key": NEWSAPI_KEY,
        "endpoints": [
            {
                "name": "Technology News",
                "query": "technology OR software OR tech startups OR artificial intelligence",
                "category": "Technology",
                "language": "en",
                "sort_by": "relevancy",
            },
            {
                "name": "Business News",
                "query": "economy OR business OR stock market OR finance",
                "category": "Business & Economy",
                "language": "en",
                "sort_by": "relevancy",
            },
            {
                "name": "Politics News",
                "query": "politics OR government OR policy OR election",
                "category": "Global Politics",
                "language": "en",
                "sort_by": "relevancy",
            },
            {
                "name": "Science News",
                "query": "science OR research OR breakthrough",
                "category": "Science",
                "language": "en",
                "sort_by": "relevancy",
            },
        ],
    },
    "rss": {
        "enabled": True,
        "sources": [
            {
                "name": "Google News - Technology",
                "url": "https://news.google.com/rss/search?q=technology&hl=en-US&gl=US&ceid=US:en",
                "category": "Technology",
            },
            {
                "name": "Google News - Business",
                "url": "https://news.google.com/rss/search?q=business%20economy%20stock%20market&hl=en-US&gl=US&ceid=US:en",
                "category": "Business & Economy",
            },
            {
                "name": "Google News - Politics",
                "url": "https://news.google.com/rss/search?q=politics%20government%20policy&hl=en-US&gl=US&ceid=US:en",
                "category": "Global Politics",
            },
            {
                "name": "Google News - Science",
                "url": "https://news.google.com/rss/search?q=science%20research%20breakthrough&hl=en-US&gl=US&ceid=US:en",
                "category": "Science",
            },
            {
                "name": "TechCrunch",
                "url": "https://techcrunch.com/feed/",
                "category": "Technology",
            },
        ],
    },
}

# Category allocation for the daily email
# Total target: 10 articles
CATEGORY_ARTICLE_COUNT = {
    "Technology": 3,
    "Business & Economy": 3,
    "Global Politics": 3,
    "Science": 1,
}

# Priority Topics (higher score = higher priority)
PRIORITY_TOPICS = {
    "OpenAI": 10,
    "Google": 9,
    "Microsoft": 9,
    "NVIDIA": 9,
    "Anthropic": 10,
    "ChatGPT": 9,
    "Claude": 9,
    "GPT": 8,
    "LLM": 8,
    "large language model": 8,
    "AI tools": 7,
    "AI startup": 7,
    "US economy": 8,
    "stock market": 7,
    "market": 6,
    "breakthrough": 6,
    "research": 5,
    "innovation": 5,
    "algorithm": 5,
}

# Categories
CATEGORIES = [
    "Technology",
    "Business & Economy",
    "Global Politics",
    "Science",
]

# Email Configuration
EMAIL_CONFIG = {
    "sender_email": os.getenv("SENDER_EMAIL", ""),
    "sender_password": os.getenv("SENDER_PASSWORD", ""),
    "sender_name": "Daily Tech News Digest",
    "subject_template": "Daily Tech News Digest - {date}",
    "recipient_email": RECIPIENT_EMAIL,
    "max_articles": 10,
    "articles_per_category": CATEGORY_ARTICLE_COUNT,
}

# SMTP Configuration
SMTP_CONFIG = {
    "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "port": int(os.getenv("SMTP_PORT", "587")),
}

# Time Configuration (US Eastern Time)
TIME_CONFIG = {
    "timezone": "America/New_York",
    "send_time": "09:00",
    "look_back_hours": 24,
}

# Article Filtering
ARTICLE_FILTERS = {
    "min_word_count": 5,
    "exclude_keywords": ["advertisement", "sponsored", "press release"],
    "required_fields": ["title", "description", "url", "source"],
}
