import sqlite3

class DB_handle():
    """A handle to communicate with the sqlite database"""

    def __init__(self, db_name):
        # Instance have DB name
        self.db = db_name
        
        # Initiate the database
        self.initiate_db(self.db)
        
    def initiate_db(self, db_name):
        """A method which checks if we have a DB and table or creates a new one"""

        # Cursor to DB
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        sql_cmd = """
        CREATE TABLE IF NOT EXISTS tweets (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        tweet_id TEXT NOT NULL,
        created_at REAL NOT NULL,
        lang TEXT NOT NULL,
        retweet INTEGER NOT NULL,
        text TEXT NOT NULL,
        source TEXT NOT NULL,
        key_word TEXT NOT NULL,
        sentiment TEXT,
        tokens TEXT);
        """

        cur.execute(sql_cmd)
    
    def addTweets(self, list_of_tweets, keyword):
        """A method which adds tweets to DB if they are not in the DB"""
        
        # Connect to DB
        conn = sqlite3.connect(self.db)
        # Pointer
        cur = conn.cursor()

        # Add tweets
        for tweet in list_of_tweets:
            # Skip if we have the tweet
            # MAKE SURE THIS IS WORKING ..
            
            if cur.execute('SELECT EXISTS(SELECT 1 FROM tweets WHERE tweet_id=(?) LIMIT 1)', (str(tweet.id),)) is True:
                continue
            # Insert tweet in DB
            else:
                cur.execute('''INSERT INTO tweets (tweet_id, created_at, lang, retweet, text, source, key_word) VALUES (?, ?, ?, ?, ?, ?, ?)''', (tweet.id, tweet.created_at, tweet.lang, tweet.retweeted, tweet.text, tweet.source_url, keyword))

        conn.commit()
        conn.close()

    def get_no_sentiment(self):
        """Returns tweets from DB which doesn't have a sentiment"""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        cur.execute('SELECT * FROM tweets WHERE sentiment is NULL')

        tweets = cur.fetchall()

        conn.close()
        return tweets

    def set_sentiment(self, db_id, sentiment):
        """Set the sentiment for a given tweet byt its ID"""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        cur.execute("UPDATE tweets SET sentiment=? WHERE Id=?", (sentiment, db_id))
        conn.commit()
        conn.close()

    def get_sentiment(self):
        """Returns tweets from DB which have a sentiment"""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        cur.execute('SELECT * FROM tweets WHERE sentiment is NOT NULL')

        tweets = cur.fetchall()

        conn.close()
        return tweets

    def add_tokens(self, db_id, tokens):
        """Add tokens to the tokens column in DB"""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        cur.execute("UPDATE tweets SET tokens=? WHERE Id=?", (tokens, db_id))

        conn.commit()
        conn.close()
