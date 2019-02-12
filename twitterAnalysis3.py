import pickle
import os
# import twitter
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import KotakNityo.sentiment_mod2 as s

# Get Acess to the twitter and Make Object.
p1 = 'secret_twitter_credentials.pkl'  # This file is available in my repository for confidential.
# os.remove(p1)  # use this command if you have regenerate Twitter attributes as mentioned below
Twitter = pickle.load(open(p1,'rb'))  # if .pkl file exist then just read it into Twitter object


# Authentication Step for acceseing Data-------------------------------------------------------------------------------
auth = OAuthHandler(Twitter['Consumer Key'], Twitter['Consumer Secret'])
auth.set_access_token(Twitter['Access Token'], Twitter['Access Token Secret'])


#consumer key, consumer secret, access token, access secret.


class listener(StreamListener):

        def on_data(self, data):
            try:
                all_data = json.loads(data)
                saveFile = open('tweetStore.txt','a')
                saveFile.write(str(all_data))
                saveFile.write('\n')
                saveFile.close()
                #print("all_data"+str(all_data))
                if 'text' not in all_data:
                    return True
                tweet = all_data["text"]
                sentiment_value, confidence = s.sentiment(tweet)
                print(tweet, sentiment_value, confidence)

                if confidence*100 >= 80:
                    output = open("twitter-out.txt","a")
                    output.write(sentiment_value)
                    output.write('\n')
                    output.close()
                return True
            except:
                return True

        def on_error(self, status):
            print(status)
            return True


def start_stream(text):
    while True:
        try:
            twitterStream = Stream(auth, listener())
            twitterStream.filter(track=[text])
        except:
                continue


start_stream("narendramodi")  # Here mention text of your interest


