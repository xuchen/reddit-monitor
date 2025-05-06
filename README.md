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

### Oracle Cloud Free

First register for Oracle Cloud. You do need to associate with a credit card.
They said they won't charge me in their free plan.

Their Always Free plan has:

1. AMD Compute Instance -- AMD based Compute VMs with 1/8 OCPU and 1 GB memory each -- Always Free -- 2 AMD based compute VMs
2. Arm Compute Instance -- Arm-based Ampere A1 cores and 24 GB of memory usable as 1 VM or up to 4 VMs -- Always Free -- 3,000 OCPU hours and 18,000 GB hours per month

First create your instance, make sure to upload your public SSH key.

When creating your instance, make sure to select the Free tier. Their cost analysis will show $2/month for boot volume. This should be a known bug.

After it's up and runnning, assign a public IPv4 address, copy it, and then:

`ssh ubuntu@<ip address>`

Once you log in, you can do the following:

```
git clone https://github.com/xuchen/reddit-monitor.git
cd reddit-monitor
sudo apt-get install python3-pip
pip install --break-system-packages -r requirements.txt

Note that the last step is a quick and dirty way to install all dependencies.

Now you need to edit the .env file with your reddit and sendgrid credentials.
After that, you can run the command: `nohup python3 reddit-monitor.py`

Now your system should be up and running!

### PythonAnywhere

Note: it turned out that PythonAnywhere only gives you 100s of CPU time every day.
It's far less than enough.

I use the pythonanywhere.com's free account. Note that free account restricts
outbound internet access from a [whitelist](https://www.pythonanywhere.com/whitelist/). Luckily both Reddit and Sendgrid are on the list.

Simply follow the "I want to clone and hack on my GitHub project" tutorial 
from pythonanywhere.com after creating the account, to clone your repo and run
`python reddit_monitor.py` from the console. Then you are all set!