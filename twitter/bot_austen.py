import tweepy

exec(open("./config").read())

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

exec(open("./twitter_austen.py").read())

INTERVAL = 12*60*60
#INTERVAL = 5*60 # for testing

while True:
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
    generate_tweet(printing=True)
    time.sleep(INTERVAL)
