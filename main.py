#!/usr/bin/env python
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):

    def __init__(self):
        consumer_key = 'fBY3F2WoEB3wuhKj3hF0EpMGw'
        consumer_secret = 'nxANBeFjsrqrZwE6QwGbGtPQk94BbUyqDtxrEcFgAroWdDQ6AY'
        access_token = '1124239882451243008-gsKVvE4GCnUgZiEp4tUGcNbSauadP4'
        access_token_secret = 'QYsfjExdZi7WlHqhKi4cDV5NZgoc1cZ5tp2illp309GzU'

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)

            self.auth.set_access_token(access_token, access_token_secret)

            self.api = tweepy.API(self.auth)
        except Exception as e:
            print(str(e))

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


    def get_tweets(self, query, count=10):
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q= query, count = count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet                
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():
    api = TwitterClient()

    tweets = api.get_tweets(query='Bitcoin', count=1000000)

# Positive tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

# Negative tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])


if __name__ == '__main__':
    main()
