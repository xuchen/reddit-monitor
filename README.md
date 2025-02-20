# Reddit Keyword Monitor

Get email notifications when specific keywords are mentioned on Reddit using SendGrid.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/xuchen/reddit-monitor.git
   cd reddit-monitor

Install dependencies

pip install -r requirements.txt

Configure environment variables

Rename .env.template to .env

Get Reddit API credentials:

Create a Reddit app: https://www.reddit.com/prefs/apps

Use "script" type application

Get SendGrid API key:

Create account at https://sendgrid.com

Verify sender email in SendGrid dashboard

Create API key with "Mail Send" permissions

Modify configuration

Update KEYWORDS and SUBREDDITS in reddit_monitor.py if needed

Adjust CHECK_INTERVAL (in seconds) as desired

Run the monitor

python reddit_monitor.py

## New Features
- Keywords loaded from `keywords.txt` file
- Automatic reload when keywords file changes
- Comments in keywords file using #
- Thread-safe operations

## Usage
1. Edit `keywords.txt` while the program is running
2. Save changes - the program will auto-detect updates
3. Add/remove keywords without restarting
4. Use comments in the file with `#`

## How to Run Locally

```
# Install dependencies
pip install -r requirements.txt

# Create and populate .env file
cp .env.template .env
# Edit .env with your credentials

# Create keywords file
touch keywords.txt
# Add your keywords

# Run the monitor
python reddit_monitor.py
```

## How to Run on the cloud For Free

I use the pythonanywhere.com's free account. Note that free account restricts
outbound internet access from a [whitelist](https://www.pythonanywhere.com/whitelist/). Luckily both Reddit and Sendgrid are on the list.

Simply follow the "I want to clone and hack on my GitHub project" tutorial 
from pythonanywhere.com after creating the account, to clone your repo and run
`python reddit_monitor.py` from the console. Then you are all set!