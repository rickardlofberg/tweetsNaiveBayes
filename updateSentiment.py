import tweetData
from settings import DB_name as DB

if __name__ == '__main__':
    # Possible sentiments
    pos_sent = set(['pos', 'neg', 'neu'])
    
    # Get handle
    db_handle = tweetData.DB_handle(DB)

    tweets = db_handle.get_no_sentiment()

    for tweet in tweets:
        sent = ''

        print(tweet[5], '\n')

        # Until we get a valid sentiment
        while sent not in pos_sent:
            sent = input("Is this pos, neg or neu? ")

        db_handle.set_sentiment(tweet[0], sent)

        print()
            
    print('No more tweets to assign sentiment to.')
