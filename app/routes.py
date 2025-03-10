from flask import Blueprint, render_template, request, jsonify, current_app
from flask_mail import Message
from app.ai import AI
from app.models import Tweet
from app.scheduler import tweet_scheduler 
from app.email_automation import send_email
import random
import os 
import re

main_bp = Blueprint('main', __name__)

# In-memory tweet storage (for demonstration)
tweets = []
auto_tweet_count = 0  # Global counter for automated tweets


def remove_emojis(text):
    emoji_pattern = re.compile("[\U00010000-\U0010FFFF]", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def send_email_notification(recipient, tweet):
    print("Tweet: ",tweet)
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv('SENDER_PASSWORD')
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    tweet['content'] = remove_emojis(tweet['content'])
    subject = f"Tweet Posted on {tweet['title']} "
    body = (f"Your automated tweet was posted:\n\n"
                f"Title: {tweet['title']}\n"
                f"Content: {tweet['content']}\n"
                f"Hashtags: {', '.join(tweet['hashtags'])}\n"
                f"Timestamp: {tweet['timestamp']}")
    
    send_email(smtp_server, smtp_port, sender_email, sender_password,
                       recipient, subject, body)


@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/post_tweet', methods=['POST'])
def post_tweet():
    mode = request.form.get('mode', 'manual')
    # For single tweet posting:
    if mode == 'manual':
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        hashtags = request.form.get('hashtags', '').split(',')
        tweet = Tweet(title, content, [h.strip() for h in hashtags if h.strip()])
        tweet_data = tweet.to_string()
        tweet.tweet_post(tweet_data)
        return jsonify({'message': 'Tweet posted manually!', 'tweet': tweet.to_dict()})
    
    elif mode == 'auto':
        try:
            interval = int(request.form.get('interval', 60))
        except ValueError:
            return jsonify({'message': 'Invalid interval value'}), 400
        email = request.form.get('email', '')
        topic = request.form.get('topic', '').split(',')
        if not email or not topic:
            return jsonify({'message': 'Email and topic are required for auto mode'}), 400
        # Schedule the automated tweet.
        tweet_scheduler.schedule_tweet(interval, auto_post_tweet, email, topic)
        return jsonify({'message': f'Automatic tweet posting scheduled every {interval} seconds!', 'interval': interval})
    else:
        return jsonify({'message': 'Invalid mode'}), 400

@main_bp.route('/generate_tweets', methods=['GET'])
def generate_tweets():
    title = request.args.get('title', '')
    content = request.args.get('content', '')
    hashtags = request.args.get('hashtags', '').split(',') if request.args.get('hashtags') else []
    # print("hashtags: ", hashtags)
    tweet = AI.generate_tweet(title, content=content, hashtag=hashtags)
    return tweet

def auto_post_tweet(email, topics):
    global auto_tweet_count
    topic = random.choice(topics)
    tweet_data = AI.generate_tweet(topic)
    tweet = Tweet(tweet_data['title'], tweet_data['content'], tweet_data['hashtags'])
    tweet_string = tweet.to_string()
    print("Tweet String: ",tweet_string)
    tweet_dict = tweet.to_dict()
    # Send email notification
    send_email_notification(email, tweet_dict)
    tweet.tweet_post(tweet_string)
    auto_tweet_count += 1
    print("Tweet Posted...")
    # tweets.append(tweet_dict)
   

@main_bp.route('/auto_count', methods=['GET'])
def auto_count():
    return jsonify({'auto_tweet_count': auto_tweet_count})
