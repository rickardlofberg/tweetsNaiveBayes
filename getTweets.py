import tweetData
import tweepy
import keys
from settings import DB_name as DB
import sys

# Run program as main
if __name__ == '__main__':
    try:
        # Set login details (set in file keys.py)
        auth = tweepy.OAuthHandler(keys.consumer_token, keys.consumer_secret)
        auth.set_access_token(keys.access_token, keys.access_secret)
            
        # Connect to twitter
        api = tweepy.API(auth)

        connected = True
    except:
        print('Something went wrong with the connection to twitter.')
        print('Make sure you have tweepy installed and vallid authentication data.')
        connected = False

    # If connected to Twitter API
    if connected:
        # Check args 
        if len(sys.argv) > 1:
            # First arg is keyword (without pound-sign)
            keyword = sys.argv[1]
            # Second arg is number of tweets
        if len(sys.argv) > 2:
            # Escape invalid input
            try:
                number_of_tweets = int(sys.argv[2])
            except:
                print("The second argument needs to be an integer")
        # Get 10 tweets as standard
        else:
            number_of_tweets = 10

        # Third argument is langauge
        if len(sys.argv) > 3:
            lang = sys.argv[3]
        else:
            lang = 'en'
        
        try:
            # Get tweets by seach keyword
            tweets = tweepy.Cursor(api.search, q=keyword, lang=lang).items(number_of_tweets)
        except:
            print('Something went wrong when retriving tweets')

        # DB handle
        db_handle = tweetData.DB_handle(DB)
        
        # Add tweets to DB
        try:
            found_tweets = 0
            list_of_tweets = []
            for tweet in tweets:
                found_tweets += 1
                list_of_tweets.append(tweet)
            db_handle.addTweets(list_of_tweets, keyword)
            print('{} tweets has been added to the DB'.format(found_tweets))
        except:
                print("Couldn't add tweets to DB.")
                
