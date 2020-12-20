from operator import itemgetter
import operator
from models import Person
import tweepy
from datetime import datetime, date, time, timedelta

people = []

def twitter(screen_name):
    for person in people:
        if person.screen_name == screen_name:
            return person.__dict__

    api = get_api()

    user = None
    try:
        user = api.get_user(screen_name)
    except tweepy.error.TweepError:
        return {"Error":"Username Not Found"}
    tweets_count = user.statuses_count
    account_created_date = user.created_at
    followers_count = user.followers_count
    days = (datetime.utcnow() - account_created_date).days

    timeline = []
    for status in tweepy.Cursor(api.user_timeline, screen_name='@'+screen_name).items():
        timeline.append({"text":status._json["text"],"created_at":status._json["created_at"],"retweet_count":status._json["retweet_count"]})
    avg = float(tweets_count)/float(days)
    timeline = sorted(timeline, key=lambda item: item.get("retweet_count"), reverse=True)
    populars = []
    for i in range(0,10):
         populars.append(timeline[i])
    person = Person(screen_name,tweets_count,followers_count,days,timeline,avg, populars)
    people.append(person)
    return person.__dict__

def get_api():
    consumer_key = 'cphCQBLvEOcd3ZuNO8GCvXvud'
    consumer_secret = 'SDVHR7mWYyHhxAH6TArslXmuCfwpbaLAa6TWEmeyW7eYinpFJk'

    access_token = '1331451724071055366-so1EprYFjh8hW7CnDDxocffz8KSlOp'
    access_token_secret = 'nhLanJ5J7SBBPsKDgeLQHXcR98PUHOCxcEVBjFYFfPXMT'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)
