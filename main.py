#import time
#start = time.time()
import json
import numpy as np
import keras
import tensorflow as tf
import keras.preprocessing.text as kpt
from keras.models import model_from_json
import re
import tweepy
from tweepy import OAuthHandler
from keras.preprocessing.text import Tokenizer
from keras import backend as K
#import psutil
import os
# Load our dictionary file
with open('dictionary.json', 'r') as dict_file:
    dictionary = json.load(dict_file)


def convert_text_to_index_array(text):
        words = kpt.text_to_word_sequence(text)
        wordIndices = []
        for word in words:
            if word in dictionary:
                wordIndices.append(dictionary[word])
        return wordIndices

# num_words is the maximum number of words that will be considered by our algorithm
tokenizer = Tokenizer(num_words=1000)

# Load model
json_file = open('1000w-model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

model = model_from_json(loaded_model_json)
model.load_weights('1000w-model.h5')
graph = tf.get_default_graph()

# These are our categories/labels
labels = ['negative', 'positive',]
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

    
# Get user input and make a prediction on that input. Then return that prediction to the user.
    def get_tweet_sentiment(self, tweet):
        evalSent = self.clean_tweet(tweet)
        testArr = convert_text_to_index_array(self.clean_tweet(tweet))
        uinput = tokenizer.sequences_to_matrix([testArr], mode='binary')
        global graph
        with graph.as_default():
                model._make_predict_function()
                pred = model.predict(uinput) 
        #print("%s sentiment; %f%% confidence" % (labels[np.argmax(pred)], pred[0][np.argmax(pred)] * 100))
        if labels[np.argmax(pred)] == 'positive' and pred[0][np.argmax(pred)] > 0.5:
            return 'positive'
        elif labels[np.argmax(pred)] == 'negative' and pred[0][np.argmax(pred)] > 0.5:
            return 'negative'
        else:
            return 'neutral'

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
#process = psutil.Process(os.getpid())
#print("Total memory used")
#print(process.memory_info().rss)      
#end = time.time()
#print("Total time taken")
#print(end - start)
if __name__ == '__main__':
    main()

    
