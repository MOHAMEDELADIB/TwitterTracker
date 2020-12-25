import json
import threading
import time

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from accounts.utils import tweets_email
from twitter import twitter_credentials

# # # # TWITTER STREAMER # # # #

isclicked = False


def update_stream(stream):
    if stream.running is True:
        stream.disconnect()
        return False
    else:
        return True


class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        pass

    def stream_tweets(self, postive_words, negative_words, email, username):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        global isclicked
        listener = StdOutListener(postive_words, negative_words, email)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener, wait_on_rate_limit=True)
        update_stream(stream)
        condition = True
        # This line filter Twitter Streams to capture data by the keywords:
        while condition:
            condition = isclicked
            if stream.running is True:
                stream.disconnect()

            else:
                isclicked = False
                time.sleep(5)
                isclicked = True
                IDS = []
                for element in getuserdata(username):
                    IDS.append(str(element))
                stream.filter(follow=IDS,
                              encoding='utf-8',
                              is_async=True)  # Open the stream to work on asynchronously on a different thread
                time.sleep(7200)
        stream.disconnect()


# # # # TWITTER STREAM LISTENER # # # #
def sendmail(s, postive_words, negative_words, Email):
    word1 = []
    word2 = []
    word1 = postive(postive_words.lower())
    word2 = negative(negative_words.lower())
    if word1[0] == '': word1 = []
    if word2[0] == '': word2 = []
    text = s['text']
    text = text.lower()

    if len(word1) > 0 and len(word2) > 0:
        for element in word1:
            lower_element = element.lower()
            if lower_element in text:
                for element2 in word2:
                    lower_element2 = element2.lower()
                    if lower_element2 in text:
                        tweets_email(Email, s['text'])
                        print(s['text'])
                        time.sleep(1)

    if len(word1) > 0 and len(word2) < 1:
        for element in word1:
            lower_element = element.lower()
            if lower_element in text:
                tweets_email(Email, s['text'])
                print(s['text'])
                time.sleep(1)
    if len(word1) < 1 and len(word2) > 0:
        for element in word2:
            lower_element = element.lower()
            if lower_element in text:
                tweets_email(Email, s['text'])
                print(s['text'])
                time.sleep(1)
def getclicked():
    global isclicked
    return isclicked


class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, postive_words, negative_words, email):

        super().__init__()
        self.postive_words = postive_words
        self.negative_words = negative_words
        self.email = email

    def on_data(self, data):
        try:
            s = json.loads(data)
            sendmail(s, self.postive_words, self.negative_words, self.email)
            return getclicked()
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        time.sleep(120)
        return True

    def on_timeout(self):
        return True


def getuserdata(username):
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    ids = []
    for page in tweepy.Cursor(api.friends_ids, screen_name=username).pages():
        ids.extend(page)
    return ids


def postive(postive_words):
    postive = postive_words.split(",")
    return postive


def negative(negative_words):
    negative = negative_words.split(",")
    return negative


def disconnect(x):
    global isclicked
    isclicked = x
    return isclicked


def stop_stream():
    global isclicked
    isclicked = False
    print(isclicked)
    time.sleep(5)


def user_isvalid(username):
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, timeout=5)
    try:
        return True
    except:
        return False


def mainfunction(postive_words: str, negative_words: str, username, email):
    global isclicked
    isclicked = False
    time.sleep(10)
    isclicked = True
    IDS = []

    # Authenticate using config.py and connect to Twitter Streaming API.
    twitter_streamer = TwitterStreamer()
    for element in getuserdata(username):
        IDS.append(str(element))

    download_thread = threading.Thread(target=twitter_streamer.stream_tweets, name="Downloader",
                                       args=(postive_words, negative_words, email, username))

    if download_thread.is_alive():
        download_thread.join()
    if not download_thread.is_alive():
        download_thread.start()
