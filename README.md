# Daily Tech News Aggregator

Automated daily news digest service that collects tech, AI, science, and business news from multiple sources and sends a curated email report.

## Features

- 📰 **Multi-source aggregation**: NewsAPI, Google News, TechCrunch, Reuters
- 🎯 **Smart prioritization**: AI-powered ranking based on topic relevance
- 📧 **Beautiful HTML emails**: Professional formatted daily digest
- 🤖 **Fully automated**: Runs daily at 9 AM EST via GitHub Actions
- 🔄 **Deduplication**: Automatically removes duplicate articles
- 📱 **Mobile friendly**: Responsive email design

## News Categories

- Artificial Intelligence
- Technology
- Science
- Business & Economy
- Global Politics

## Priority Topics

Articles mentioning these topics receive higher priority:
- OpenAI, Google, Microsoft, NVIDIA, Anthropic
- ChatGPT, Claude, GPT, Large Language Models
- AI tools and startups
- US economy and stock market
- Scientific breakthroughs

## Quick Start

### Prerequisites

1. **NewsAPI Key**: Sign up at [newsapi.org](https://newsapi.org)
2. **Email Service**: Choose one:
   - **SendGrid** (recommended): [sendgrid.com](https://sendgrid.com)
   - **Gmail SMTP**: Your Gmail account with app password

### Setup Instructions

1. **Clone and navigate to the repository**
   ```bash
   git clone https://github.com/WingHuang666/project-01.git
   cd project-01
   ```

2. **Add GitHub Secrets**
   - Go to: **Settings** → **Secrets and variables** → **Actions**
   - Add these secrets:

   **Required:**
   - `NEWSAPI_KEY` = Your NewsAPI key
   - `RECIPIENT_EMAIL` = huangwing666@gmail.com

   **For SendGrid (Recommended):**
   - `SENDGRID_API_KEY` = Your SendGrid API key

   **OR For Gmail SMTP:**
   - `SENDER_EMAIL` = your-email@gmail.com
   - `SENDER_PASSWORD` = Gmail app password
   - `SMTP_SERVER` = smtp.gmail.com
   - `SMTP_PORT` = 587

3. **Test Manually**
   - Go to **Actions** tab
   - Click **Daily News Digest**
   - Click **Run workflow** → **Run workflow**
   - Check your email in ~2 minutes

## Configuration

Edit `news_aggregator/config.py` to customize:

- **Send time**: Change `cron` in `.github/workflows/daily-news-digest.yml`
- **Article count**: Modify `max_articles` in `config.py`
- **Priority topics**: Add/remove topics in `PRIORITY_TOPICS`
- **News sources**: Enable/disable sources in `NEWS_SOURCES`

## Project Structure

```
project-01/
├── news_aggregator/
│   ├── config.py           # Configuration & settings
│   ├── news_fetcher.py     # Fetch & rank news articles
│   ├── email_sender.py     # Format & send emails
│   ├── main.py             # Main orchestrator
│   └── requirements.txt     # Python dependencies
├── .github/
│   └── workflows/
│       └── daily-news-digest.yml  # GitHub Actions workflow
├── .gitignore
└── README.md
```

## How It Works

1. **Fetch** articles from 4 news sources
2. **Filter** by category and quality
3. **Rank** by priority score (OpenAI, Google, Microsoft, NVIDIA, etc.)
4. **Select** top 10 articles
5. **Format** beautiful HTML email
6. **Send** to your inbox at 9 AM EST daily

## Timezone

- **Cron Schedule**: 9 AM EST (14:00 UTC)
- **Email Date**: US Eastern Time
- **Customizable**: Edit cron in workflow file to change time

## Troubleshooting

### No email received?
1. Check GitHub Actions logs: **Actions** → **Daily News Digest** → Latest run
2. Verify API keys are correct in GitHub Secrets
3. Check spam/junk folder
4. Ensure `RECIPIENT_EMAIL` is correct

### No articles found?
1. Verify `NEWSAPI_KEY` is valid
2. Check internet connection in GitHub Actions
3. Review logs in Actions tab for API errors

### Email formatting issues?
1. Email client may not support advanced HTML
2. Try opening in different email client
3. Check browser version if viewing in webmail

## API Limits

- **NewsAPI**: 100 requests/day (free tier)
- **SendGrid**: 100 emails/day (free tier)
- **GitHub Actions**: 2,000 minutes/month (free tier)

## Future Enhancements

- [ ] Add weather and cryptocurrency news
- [ ] Support multiple email recipients
- [ ] Add topic subscriptions
- [ ] Generate weekly digests
- [ ] Implement article summarization
- [ ] Add web dashboard to view archives

## License

MIT License - Feel free to use and modify!

## Support

For issues or questions, create a GitHub issue in this repository.

---

**Made with ❤️ by GitHub Copilot**
