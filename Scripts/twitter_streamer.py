import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler


 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

 
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('../json/Trump2.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error : " + str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#Trump'])