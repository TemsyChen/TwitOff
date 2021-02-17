'''Connecting to Twitter API to get real user and tweets'''

import tweepy
import spacy
from models import DB, Tweet, User
from os import getenv

#twitter api credentials
API_KEY = getenv('TWITTER_API_KEY', default='OOPS')
API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET', default='OOPS')
TWITTER_AUTH = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

#nlp model
nlp = spacy.load('my_model')


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


#a function to update the database
def add_or_update_user(username):
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)
        DB.session.add(db_user)

        #grabs the most recent 200 tweets
        tweets = twitter_user.timeline(
                 count=200, exclude_replies=True,
                 include_rts=False, tweet_mode="extended"
                 )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        #iterate through each tweet and add to the database table
        for tweet in tweets:
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text,
                             vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
            # session.rollback()
            print('Error processing{}: {}'.format(username, e))

    else:
        DB.session.commit()
