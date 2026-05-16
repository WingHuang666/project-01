# Daily Tech News Aggregator - Complete Setup Guide

## Table of Contents

1. [Getting API Keys](#getting-api-keys)
2. [GitHub Secrets Configuration](#github-secrets-configuration)
3. [Email Service Setup](#email-service-setup)
4. [Testing](#testing)
5. [Customization](#customization)
6. [Troubleshooting](#troubleshooting)

---

## Getting API Keys

### NewsAPI Key (Required)

**Step 1**: Visit [https://newsapi.org](https://newsapi.org)

**Step 2**: Click "Get API Key"

**Step 3**: Sign up for free account (no credit card required)

**Step 4**: Verify your email

**Step 5**: Copy your API key from dashboard

✅ You now have: `NEWSAPI_KEY`

---

## Email Service Setup

### Option A: SendGrid (Recommended)

#### Why SendGrid?
- ✅ More reliable
- ✅ Better deliverability
- ✅ Free tier: 100 emails/day
- ✅ Easy setup

**Step 1**: Visit [https://sendgrid.com](https://sendgrid.com)

**Step 2**: Click "Create Free Account"

**Step 3**: Complete signup with:
- Email address
- Password
- Company name

**Step 4**: Verify your email

**Step 5**: Navigate to **Settings** → **API Keys**

**Step 6**: Click **Create API Key**

**Step 7**: Give it a name (e.g., "GitHub News Aggregator")

**Step 8**: Select permissions:
- ✅ Mail Send
- ✅ (keep others unchecked for security)

**Step 9**: Copy the generated API key

✅ You now have: `SENDGRID_API_KEY`

**Sender Email**: Use `noreply@github.com` (in code, can be any email)

---

### Option B: Gmail SMTP

#### Prerequisites
- Active Gmail account

**Step 1**: Go to [myaccount.google.com/security](https://myaccount.google.com/security)

**Step 2**: Enable 2-Step Verification (if not enabled)

**Step 3**: Go to **App passwords**
   - (If you don't see this option, 2FA isn't enabled)

**Step 4**: Select:
   - App: **Mail**
   - Device: **Windows/Mac/Linux (custom)**

**Step 5**: Copy the 16-character password

✅ You now have:
- `SENDER_EMAIL` = your-email@gmail.com
- `SENDER_PASSWORD` = 16-character app password
- `SMTP_SERVER` = smtp.gmail.com
- `SMTP_PORT` = 587

---

## GitHub Secrets Configuration

**Step 1**: Open your repository

**Step 2**: Go to **Settings** tab

**Step 3**: In left sidebar, click **Secrets and variables** → **Actions**

**Step 4**: Click **New repository secret**

**Step 5**: Add each secret one by one:

### Required Secrets (All Options)

```
Name: NEWSAPI_KEY
Value: [Your NewsAPI key from step above]
```

```
Name: RECIPIENT_EMAIL
Value: huangwing666@gmail.com
```

### Choose ONE email service:

#### If using SendGrid:

```
Name: SENDGRID_API_KEY
Value: [Your SendGrid API key]
```

#### If using Gmail:

```
Name: SENDER_EMAIL
Value: your-email@gmail.com
```

```
Name: SENDER_PASSWORD
Value: [16-character Gmail app password]
```

```
Name: SMTP_SERVER
Value: smtp.gmail.com
```

```
Name: SMTP_PORT
Value: 587
```

✅ All secrets are now configured!

---

## Testing

### Manual Trigger

**Step 1**: Go to **Actions** tab in GitHub

**Step 2**: Click **Daily News Digest** workflow

**Step 3**: Click **Run workflow** dropdown

**Step 4**: Click **Run workflow** button

**Step 5**: Wait 30-60 seconds for it to start

**Step 6**: Check your email inbox in 2-3 minutes

### View Logs

**Step 1**: Click the running workflow

**Step 2**: Click **fetch-and-send-news** job

**Step 3**: Scroll through logs to see:
   - Articles fetched count
   - Priority scoring
   - Email sending status

### Troubleshooting Tests

If no email received:

1. **Check API Key**: Is NEWSAPI_KEY valid?
   - Look for: "Fetched X articles from NewsAPI"
   - Error: "401 Unauthorized" = bad key

2. **Check Email Config**: Did it send?
   - SendGrid: "Email sent successfully via SendGrid"
   - Gmail: "Email sent successfully via SMTP"

3. **Check Recipient**: Is email address correct?
   - Verify in logs: "Sending email digest to..."

4. **Check Spam**: Email might be in spam folder
   - Check junk/spam in your email client

---

## Customization

### Change Schedule Time

**File**: `.github/workflows/daily-news-digest.yml`

**Find line** (around line 7):
```yaml
cron: '0 14 * * *'
```

**Change to your desired time**:
- `'0 14 * * *'` = 9 AM EST (current)
- `'0 18 * * *'` = 1 PM EST
- `'0 22 * * *'` = 5 PM EST
- `'0 6 * * *'` = 1 AM EST

**Format**: `'MM HH * * *'` where HH is UTC hour

**Cron converter**: [crontab.guru](https://crontab.guru)

### Change Priority Topics

**File**: `news_aggregator/config.py`

**Find section** (around line 70):
```python
PRIORITY_TOPICS = {
    'OpenAI': 10,
    'Google': 9,
    # ...
}
```

**Add/modify topics**:
```python
PRIORITY_TOPICS = {
    'OpenAI': 10,        # Higher number = higher priority
    'MyCompany': 8,      # New company
    'blockchain': 5,     # New topic
}
```

### Change Article Count

**File**: `news_aggregator/config.py`

**Find line** (around line 105):
```python
'max_articles': 10,
```

**Change to your preference**:
```python
'max_articles': 15,  # Now sends 15 articles per day
```

### Add/Remove News Sources

**File**: `news_aggregator/config.py`

**For NewsAPI sources** (around line 20):
```python
'endpoints': [
    {
        'name': 'Blockchain News',
        'query': 'blockchain OR cryptocurrency',
        'category': 'Technology',
        'language': 'en',
        'sort_by': 'relevancy'
    },
    # Add more endpoints here
]
```

**For RSS sources** (around line 50):
```python
'sources': [
    {
        'name': 'My Custom Feed',
        'url': 'https://example.com/feed.xml',
        'category': 'Technology'
    },
    # Add more RSS feeds here
]
```

### Change Recipient Email

**Option 1**: Update secret in GitHub (Recommended)
- Go to Settings → Secrets → Edit RECIPIENT_EMAIL

**Option 2**: Update in config.py
- Find `RECIPIENT_EMAIL` in `news_aggregator/config.py`
- Change to your email

---

## Troubleshooting

### Issue: "No articles fetched"

**Cause**: NewsAPI key is invalid or expired

**Fix**:
1. Verify key at [newsapi.org/dashboard](https://newsapi.org/dashboard)
2. Check key didn't expire
3. Update `NEWSAPI_KEY` secret in GitHub

---

### Issue: "Email not sending"

**Cause**: Email configuration error

**Fix for SendGrid**:
1. Verify API key is valid at sendgrid.com dashboard
2. Check secret name is exactly `SENDGRID_API_KEY`

**Fix for Gmail**:
1. Verify 2FA is enabled
2. Verify app password is 16 characters
3. Check SMTP_PORT is exactly `587`
4. Check SMTP_SERVER is exactly `smtp.gmail.com`

---

### Issue: "Email in spam folder"

**Cause**: Email reputation or SPF/DKIM issues

**Fix**:
1. Mark email as "Not Spam"
2. Add sender to contacts
3. Use SendGrid (better deliverability)

---

### Issue: "Wrong timezone"

**Cause**: Cron uses UTC, not EST

**Fix**: Update cron schedule
- Current: `0 14 * * *` (9 AM EST = 14:00 UTC)
- For 9 AM PST: `0 17 * * *`
- For 9 AM GMT: `0 9 * * *`

---

### Issue: "Too many/too few articles"

**Fix 1**: Adjust `max_articles` in config.py

**Fix 2**: Adjust priority threshold
- Edit `PRIORITY_TOPICS` weights
- Higher weights = more articles selected

---

## Next Steps

✅ **Setup complete!**

- Monitor first digest at scheduled time
- Check GitHub Actions logs
- Customize as needed
- Enjoy your daily tech news! 🎉

---

## Need Help?

1. Check GitHub Actions logs for error messages
2. Review this guide again
3. Create GitHub issue with:
   - Error message from logs
   - Screenshots
   - What you've tried

**Happy news reading! 🎉**