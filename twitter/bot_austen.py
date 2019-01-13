import tweepy
from apscheduler.schedulers.background import BackgroundScheduler

exec(open("./config").read())
exec(open("./twitter_austen.py").read())

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

INTERVAL = 12*60*60
#INTERVAL = 5*60 # for testing

while True:
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
    generate_tweet(printing=True)
    time.sleep(INTERVAL)
