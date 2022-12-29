import os
# import config
import tweepy

# TODO: change all the twitter info since you can find it in the commit history!!
api = tweepy.Client(consumer_key=os.environ['apiKey'],
                    consumer_secret=os.environ['apiKeySecret'],
                    access_token=os.environ['accessToken'],
                    access_token_secret=os.environ['accessTokenSecret'])


def tweet(matchscore):
  api.create_tweet(text=matchscore)
