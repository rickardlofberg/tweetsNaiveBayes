import sqlite3
import nltk
import random
import sys
from settings import DB_name as DB

def get_tweets(data_base, limit=100):
    """Retrive # of tweets from DB, return them as a list of
    positive tweets and negative tweets"""
    
    # Get tweets from DB
    conn = sqlite3.connect(data_base)
    cur = conn.cursor()
    
    # Get positive
    cur.execute('SELECT * FROM tweets WHERE sentiment="pos" LIMIT ?', (limit,))
    posTweets = cur.fetchall()
    
    # Get negative
    cur.execute('SELECT * FROM tweets WHERE sentiment="neg" LIMIT ?', (limit,))
    negTweets = cur.fetchall()

    return posTweets, negTweets

def divid_data(posTweets, negTweets, training_size=0.8, seed=1):
    """Mutate the current posTweets and negTweets (rmv tweets)
    which are returned in the list of testing tweets and a list
    for training"""
    
    # Set seed
    random.seed(seed)
    
    # Hold test data
    test_data = []
    
    # How much to keep as training data
    train_limit_pos = int(len(posTweets) * training_size)
    train_limit_neg = int(len(negTweets) * training_size)

    # Remove tweets from positive and add to test
    while len(posTweets) > train_limit_pos:
        test_data.append(posTweets.pop(random.randrange(0, len(posTweets))))
        
    # Remove tweets from negative and add to test        
    while len(negTweets) > train_limit_neg:
        test_data.append(negTweets.pop(random.randrange(0, len(negTweets))))
    
    # For all tweets left (training data)
    for tweet in posTweets + negTweets:
        # Get sentiment
        sent = tweet[8]
        # Split tokens and make lowercase
        tokens = tweet[9].lower().split()
        # Add to training list
        train_tweets.append((tokens, sent))
        
    return test_data, train_tweets


if __name__ == '__main__':
    # To gold args
    tweet_limit, div_size, random_seed = None, None, None
    # To hold all tweets
    train_tweets = []
    
    if len(sys.argv) > 1:
        try:
            tweet_limit = int(sys.argv[1])
        except:
            pass

    if len(sys.argv) > 2:
        try:
            div_size = float(sys.argv[2])
        except:
            pass

    if len(sys.argv) > 3:
        try:
            random_seed = int(sys.argv[3])
        except:
            pass

    # If limit selected
    if tweet_limit:
        pos, neg = get_tweets(DB, tweet_limit)
    else:
        pos, neg = get_tweets(DB)

    if div_size and random_seed:
        test, train = divid_data(pos, neg, div_size, random_seed)
    elif div_size:
        test, train = divid_data(pos, neg, div_size)
    else:
        test, train = divid_data(pos, neg)
        
    # Get features (training)
    word_features = []
    for (words, sentiment) in train:
        word_features.extend(words)
    word_features = list(set(word_features))
    
    def extract_features(document):
        """Exctract features from document (tweet) and returns them"""
        document_words = set(document)
        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features
    
    # Get training data
    training_set = nltk.classify.apply_features(extract_features, train)
    
    # Create classifier
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    
    #print(classifier.show_most_informative_features(32))
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    
    for tweet in test:
        tokens = tweet[9].lower().split()
        if classifier.classify(extract_features(tokens)) == 'pos':
            if tweet[8] == 'pos':
                TP += 1
            else:
                FP += 1
        else:
            if tweet[8] == 'pos':
                FN += 1
            else:
                FP += 1
    
    print('''
    TP: {}
    FP: {}
    TN: {}
    FN: {}
    '''.format(TP, FP, TN, FN))
