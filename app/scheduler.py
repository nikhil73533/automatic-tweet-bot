from apscheduler.schedulers.background import BackgroundScheduler

class TweetScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def schedule_tweet(self, interval, callback, *args, **kwargs):
        # Run the callback immediately

        # Schedule the callback to run at intervals
        self.scheduler.add_job(callback, 'interval', seconds=interval, args=args, kwargs=kwargs)

    def shutdown(self):
        self.scheduler.shutdown()

# Create a global scheduler instance
tweet_scheduler = TweetScheduler()
