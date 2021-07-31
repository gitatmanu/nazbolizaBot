# nazbot
Twitter bot that interacts with user mentions, sending tweet capture to them with its username changed by a randomly generated one.

## How it works?
You have to mention to the Twitter bot account (@nazbot_). Then, it will reply you with a capture of the tweet that you replied with his nickname changed.

---
## Deployment
### Dependencies
- **Firefox Browser** (Selenium WebDriver needs binaries)
- **Geckodriver** (What Selenium uses to run web browser, in 'drivers/' folder)
- **pip packages** (All in 'requirements.txt' file. To install, you need first python3-pip apt package manager. Then, install them with command 'pip install -r requirements.txt')
- **environment variables** (To connect to Twitter API and other things, you need to get the access tokens from a Twitter developer account. Then, load with an .env file and dotenv pip package.)
  - CONSUMER_KEY
  - CONSUMER_SECRET
  - ACCESS_KEY
  - ACCESS_SECRET
  - ACCOUNT_ID
  - ACCOUNT_NAME
### Execution
When you have all the dependencies, you just have to 'python3 main.py'. 
You can use a terminal multiplexer like 'screen' or 'tmux', or a python daemonizer like pip package 'python-daemon'.
