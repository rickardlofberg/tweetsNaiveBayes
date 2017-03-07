# tweetsNaiveBayes
A pipline to retrive tweets by keyword, assign sentiment, tokenize and then predict sentiment.

The pipline is as follows:

1. python3 getTweets.py [keyword] [number of tweets] [language]
2. python3 updateSentiment.py
3. python3 tweetCleaner.py
4. python3 tweetTrainer.py [pos/neg limit] [training ratio] [random seed]

NOTE: That you need to provide your own tweeter auth tokens in a file called keys.py and have tweepy installed

