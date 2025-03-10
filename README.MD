# TweetPro - Automated Tweet Posting Bot

## Overview
TweetPro is an automated tweet posting bot that leverages LLM (Large Language Model) and the Twitter API to generate and post tweets. This guide will walk you through the setup and configuration of the project.

## Prerequisites
Before setting up the project, ensure you have the following installed:

- **Python 3.10**: Download and install from [Python Official Site](https://www.python.org/downloads/release/python-3100/).
- **Visual Studio Code (VS Code)**: Download and install from [VS Code Official Site](https://code.visualstudio.com/).

## Installation Steps

### 1. Setup Virtual Environment
Open your terminal and navigate to the project directory, then execute the following command to create a virtual environment:

```sh
python -m venv venv
```

### 2. Activate Virtual Environment
#### On Windows:
```sh
venv\Scripts\activate
```
#### On macOS/Linux:
```sh
source venv/bin/activate
```

### 3. Install Required Dependencies
Run the following command to install all necessary packages from `requirements.txt`:

```sh
pip install -r requirements.txt
```

### 4. Configure Secrets
Create a `secrets.env` file in the root directory and provide the necessary secrets as follows:

#### A. Twitter Account Credentials
1. If you don’t have a Twitter account, create one at [Twitter Signup](https://twitter.com/i/flow/signup).
2. Provide your Twitter account credentials in `secrets.env`:
   ```env
   TWITTER_EMAIL=<your-twitter-email>
   TWITTER_PASSWORD=<your-twitter-password>
   TWITTER_PHONE=<your-twitter-phone-number>
   ```

#### B. Gemini Model API
1. Get the API key from [Google AI Studio](https://aistudio.google.com/prompts/new_chat).
2. Generate a new API key and add it to `secrets.env`:
   ```env
   GEMINI_API_KEY=<your-gemini-api-key>
   ```

#### C. Email Configuration
1. Use any Gmail account and generate an **App Password** following this guide: [Generate App Password](https://support.google.com/mail/answer/185833?hl=en).
2. Add the credentials to `secrets.env`:
   ```env
   EMAIL_ADDRESS=<your-email>
   EMAIL_APP_PASSWORD=<your-email-app-password>
   ```

### 5. Start the Server
Run the following command to start the TweetPro bot:

```sh
python3 run.py
```

If everything is set up correctly, the server will start running.

### 6. Access TweetPro
Once the server is running, open the application in your browser:

[Click here to open TweetPro](http://127.0.0.1:5000/#)

## Video Guide
For a step-by-step walkthrough, check out the video tutorial:
[Watch the Video](https://www.canva.com/design/DAGhWXNmT50/Pcpa8mJgW67Mc_JlgZcFsw/watch?utm_content=DAGhWXNmT50&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hd71b86410e)

## Contributing
Feel free to contribute to this project by submitting issues or pull requests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
**Happy Tweeting! 🚀**