import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmailSender:
    """Send formatted news digest via email"""
    
    def __init__(self, recipient_email: str, sendgrid_api_key: str = None):
        self.recipient_email = recipient_email
        self.sendgrid_api_key = sendgrid_api_key or os.getenv('SENDGRID_API_KEY')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', 'noreply@github.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
    
    def send_digest(self, articles: List[Dict]) -> bool:
        """Send daily digest email"""
        try:
            if not articles:
                logger.warning("No articles to send")
                return False
            
            # Generate email content
            subject = f"Daily Tech News Digest - {datetime.now().strftime('%Y-%m-%d')}"
            html_content = self._generate_html_content(articles)
            
            # Send email
            if self.sendgrid_api_key:
                return self._send_via_sendgrid(subject, html_content)
            elif self.sender_password:
                return self._send_via_smtp(subject, html_content)
            else:
                logger.error("No email service configured (SENDGRID_API_KEY or SENDER_PASSWORD)")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def _send_via_sendgrid(self, subject: str, html_content: str) -> bool:
        """Send email via SendGrid API"""
        try:
            import sendgrid
            from sendgrid.helpers.mail import Mail, Email, To, Content
            
            sg = sendgrid.SendGridAPIClient(self.sendgrid_api_key)
            
            mail = Mail(
                from_email=Email(self.sender_email, "Daily Tech News Digest"),
                to_emails=To(self.recipient_email),
                subject=subject,
                html_content=html_content
            )
            
            response = sg.send(mail)
            
            if 200 <= response.status_code < 300:
                logger.info(f"Email sent successfully via SendGrid to {self.recipient_email}")
                return True
            else:
                logger.error(f"SendGrid error: {response.status_code} - {response.body}")
                return False
                
        except ImportError:
            logger.error("sendgrid library not installed. Install with: pip install sendgrid")
            return False
        except Exception as e:
            logger.error(f"Error sending via SendGrid: {str(e)}")
            return False
    
    def _send_via_smtp(self, subject: str, html_content: str) -> bool:
        """Send email via SMTP (Gmail or other provider)"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"Daily Tech News Digest <{self.sender_email}>"
            msg['To'] = self.recipient_email
            
            # Attach HTML content
            part = MIMEText(html_content, 'html')
            msg.attach(part)
            
            # Send via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully via SMTP to {self.recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending via SMTP: {str(e)}")
            return False
    
    def _generate_html_content(self, articles: List[Dict]) -> str:
        """Generate HTML email content"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                }}
                .article {{
                    background: white;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    transition: box-shadow 0.3s ease;
                }}
                .article:hover {{
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                }}
                .article-number {{
                    display: inline-block;
                    background-color: #667eea;
                    color: white;
                    border-radius: 50%;
                    width: 30px;
                    height: 30px;
                    line-height: 30px;
                    text-align: center;
                    font-weight: bold;
                    margin-bottom: 10px;
                    font-size: 14px;
                }}
                .article-category {{
                    display: inline-block;
                    background-color: #e8f0fe;
                    color: #1967d2;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: 600;
                    margin-left: 10px;
                    text-transform: uppercase;
                }}
                .article-title {{
                    font-size: 18px;
                    font-weight: bold;
                    margin: 10px 0;
                    color: #1a73e8;
                }}
                .article-title a {{
                    color: #1a73e8;
                    text-decoration: none;
                }}
                .article-title a:hover {{
                    text-decoration: underline;
                }}
                .article-description {{
                    color: #666;
                    margin: 10px 0;
                    line-height: 1.7;
                }}
                .article-meta {{
                    font-size: 13px;
                    color: #999;
                    margin-top: 10px;
                    padding-top: 10px;
                    border-top: 1px solid #eee;
                }}
                .source {{
                    font-weight: 600;
                    color: #667eea;
                }}
                .footer {{
                    background: #f9f9f9;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    color: #999;
                    font-size: 12px;
                    margin-top: 30px;
                    border-top: 1px solid #eee;
                }}
                .priority-badge {{
                    display: inline-block;
                    background-color: #fff3cd;
                    color: #856404;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-size: 11px;
                    font-weight: bold;
                    margin-left: 5px;
                }}
                .high-priority {{
                    border-left-color: #d32f2f;
                }}
                .medium-priority {{
                    border-left-color: #ff6f00;
                }}
                .low-priority {{
                    border-left-color: #1976d2;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📰 Daily Tech News Digest</h1>
                <p>{date_str}</p>
            </div>
        """
        
        # Add articles
        for idx, article in enumerate(articles[:10], 1):  # Limit to 10 articles
            priority_score = article.get('priority_score', 0)
            priority_class = 'high-priority' if priority_score >= 10 else 'medium-priority' if priority_score >= 5 else 'low-priority'
            
            html += f"""
            <div class="article {priority_class}">
                <div>
                    <span class="article-number">{idx}</span>
                    <span class="article-category">{article['category']}</span>
                    {f'<span class="priority-badge">Priority: {priority_score}</span>' if priority_score > 0 else ''}
                </div>
                <h2 class="article-title">
                    <a href="{article['url']}" target="_blank">{article['title']}</a>
                </h2>
                <p class="article-description">{article['description']}</p>
                <div class="article-meta">
                    <span class="source">📌 Source: {article['source']}</span>
                    {f'<br>Published: {article["published_at"]}' if article.get('published_at') else ''}
                </div>
            </div>
            """
        
        # Add footer
        html += f"""
            <div class="footer">
                <p>🔔 This is an automated daily tech news digest.</p>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                <p><a href="https://github.com/WingHuang666/project-01" style="color: #667eea; text-decoration: none;">View on GitHub</a></p>
            </div>
        </body>
        </html>
        """
        
        return html
