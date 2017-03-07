import tweetData
import re
from settings import DB_name as DB

if __name__ == '__main__':

    # Create table on DB if it doesn't excists
    db_handle = tweetData.DB_handle(DB)

    tokenized = 0
    
    for tweet in db_handle.get_sentiment():
        # Keep track of tokenized tweets
        tokenized += 1
        
        # First all the tweets get cleaned

        # Remove all links
        text = re.sub(r'http[s]?://[^ ]+', ' ' ,tweet[5])
        # Remove all @
        text = re.sub(r'@[^ ]+', '', text)
        # Remove all RT
        text = re.sub(r'RT', '', text)

        # Remove &gt and &lt
        text = re.sub(r'(&gt|&lt)', '', text)

        # Remove some dates
        text = re.sub(r'[(][ 0-9-]+[)]', '', text)
        
        # Split by full-stop, space, newline and #
        text = re.split(r'[ #.,\n?!/;:-]', text)

        # Remove all empty elements
        text = [tok for tok in text if tok != '' and len(tok) > 2]

        # Change tweet to space seperated string
        text = ' '.join(text)

        # Add to Database
        db_handle.add_tokens(tweet[0], text)

    print("{} tweets have been tokenized and updated in DB.".format(tokenized))
