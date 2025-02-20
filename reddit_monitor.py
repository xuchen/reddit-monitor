from collections import deque
import os
import praw
import time
import threading
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load environment variables
load_dotenv()

# Configuration
KEYWORDS_FILE = "keywords.txt"
SUBREDDITS = "all"
CHECK_INTERVAL = 60  # Seconds between Reddit checks
FILE_CHECK_INTERVAL = 5  # Seconds between file checks
MAX_SEEN_POSTS = 10_000  # Keep last 10,000 posts in memory

# Global variables with thread safety
keywords = []
keywords_lock = threading.Lock()
last_modified = 0

# Rotating post cache
seen_posts = deque(maxlen=MAX_SEEN_POSTS)
seen_posts_lock = threading.Lock()

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def load_keywords():
    """Load keywords from file, ensuring thread safety"""
    global keywords, last_modified
    try:
        modified_time = os.path.getmtime(KEYWORDS_FILE)
        if modified_time != last_modified:
            with keywords_lock:
                with open(KEYWORDS_FILE, 'r') as f:
                    new_keywords = [line.strip() for line in f.readlines() 
                                  if line.strip() and not line.startswith('#')]
                
                # Update only if file has actually changed
                if new_keywords != keywords:
                    keywords = new_keywords
                    last_modified = modified_time
                    print(f"Loaded {len(keywords)} keywords: {', '.join(keywords)}")
    
    except Exception as e:
        print(f"Error loading keywords: {str(e)}")

class KeywordFileHandler(FileSystemEventHandler):
    """Watchdog handler for keyword file changes"""
    def on_modified(self, event):
        if event.src_path.endswith(KEYWORDS_FILE):
            load_keywords()

def start_file_watcher():
    """Start watching the keywords file for changes"""
    event_handler = KeywordFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    return observer

def send_email_via_sendgrid(subject, content):
    """Send email using SendGrid API"""
    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=os.getenv("RECIPIENT_EMAIL"),
        subject=subject,
        html_content=content)
    
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


def monitor_reddit():
    """Main Reddit monitoring function"""
    global seen_posts
    
    # Initial load of keywords
    load_keywords()
    
    # Start file watcher
    observer = start_file_watcher()
    
    try:
        while True:
            try:
                subreddit = reddit.subreddit(SUBREDDITS)
                for submission in subreddit.stream.submissions(skip_existing=True):
                    post_id = submission.id
                    
                    # Check if we've seen this post
                    with seen_posts_lock:
                        if post_id in seen_posts:
                            continue
                        seen_posts.append(post_id)
                    
                    content = f"{submission.title}\n\n{submission.selftext}".lower()
                    
                    # Check against current keywords
                    with keywords_lock:
                        current_keywords = keywords.copy()
                    
                    # Find matching keywords (case-insensitive)
                    matched_keywords = []
                    for keyword in current_keywords:
                        if keyword.lower() in content:
                            matched_keywords.append(keyword)
                    
                    if matched_keywords:
                        print(f"Match found: {submission.title}")
                        subject_keywords = ", ".join(matched_keywords)
                        email_content = f"""
                        <strong>New Reddit post matching your keywords:</strong><br><br>
                        <strong>Matched keywords:</strong> {subject_keywords}<br>
                        <strong>Title:</strong> {submission.title}<br>
                        <strong>Subreddit:</strong> {submission.subreddit.display_name}<br>
                        <strong>Author:</strong> {submission.author.name if submission.author else 'Deleted'}<br>
                        <strong>Link:</strong> <a href="{submission.url}">{submission.url}</a><br>
                        """
                        send_email_via_sendgrid(
                            f"Reddit Alert: {subject_keywords}", 
                            email_content
                        )
            
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                time.sleep(CHECK_INTERVAL)
    
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    monitor_reddit()