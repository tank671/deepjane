import tweepy
import csv
import time
import re
from fastai import *
from fastai.text import *
from pathlib import Path
from os import environ

path = Path('.')

def setup_learner():
    austen_lm = TextLMDataBunch.load(path, 'austen_lm')
    data_bunch = (TextList.from_csv(path, csv_name='blank.csv', vocab=austen_lm.vocab)
                 .random_split_by_pct()
                 .label_for_lm()
                 .databunch(bs=10))
    learn = language_model_learner(data_bunch, pretrained_model=None)
    learn.load('austen_fine')
    return learn

learn = setup_learner()

def textResponse(starter):
    csv_string = learn.predict(starter, 80, temperature=1.1, min_p=0.001)
    time.sleep(2)
    pieces = csv_string.split('.')
    pieces = '.'.join(pieces[:len(pieces)-1])+'.'
    words = pieces.split()
    for i, word in enumerate(words):
        if word == 'xxbos':
            words[i] = ''
        elif word == 'xxmaj':
            if words[i+1]:
                words[i+1] = words[i+1][0].upper() + words[i+1][1:]
            words[i] = ''
        elif word == 'xxup':
            if words[i+1]:
                words[i+1] = words[i+1].upper()
            words[i] = ''
        elif word == 'xxunk' or word == '(' or word == ')' or word == '"':
            words[i] = ''
        elif word == '.' or word == '!' or word == '?' or word == ';' or word == ',' or word == ':':
            if words[i-1]:
                words[i-1] += words[i]
            words[i] = ''
        elif word[0] == "'":
            if words[i-1]:
                words[i-1] += words[i]
            words[i] = ''
    res = ' '.join(words).strip()
    res = re.sub(r"\s+", " ", res)
    return res

def clean_tweet(text):
    if len(text) == 0:
        tweet = False
    elif len(text) > 240 or text.split()[-1] == 'Mr.' or text.split()[-1] == 'Mrs.' or text.split()[-1] == 'MR.' or text.split()[-1] == 'MRS.':
        pieces = re.split(r"[\.\!\?]", text)
        punc = re.findall(r"[\.\!\?]", text)
        weave = [pieces[i]+punc[i] for i in range(len(pieces)-2)]
        tweet = clean_tweet("".join(weave))
    else:
        tweet = text
    return tweet        

def generate_test_tweet():
    mystring = textResponse('xxbos')
    tweet = clean_tweet(mystring)
    if tweet:
        print(tweet)
    else:
        generate_test_tweet()

def generate_tweet(printing=False):
    mystring = textResponse('xxbos')
    tweet = clean_tweet(mystring)
    if tweet:
        if printing:
            print(tweet)
        api.update_status(status=tweet)
    else:
        generate_tweet()

def tweet_response(text, user, msg_id):
    starter = " ".join(text)
    res = textResponse(starter)
    res = clean_tweet(res)
    tweet = "@" + str(user) + " " + res
    api.update_status(tweet, msg_id, True)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.text.split()[0] == '@AutoAusten':
            user = status.user.screen_name
            msg_id = status.id
            starter = status.text.split()[1:]
            print(msg_id)
            tweet_response(starter, user, msg_id)
      
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['@AutoAusten'], is_async=True)


