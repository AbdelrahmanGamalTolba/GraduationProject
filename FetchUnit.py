# FetchUnit
# Description: Fetches Tweets from the internet, extract different tweet features and output them to the database
# Inputs: Keyword, Number of tweets
# Outputs: Print Tweets (Tweet text, User ID, Tweet ID, No. of RETWEETS, No. of favorites, Tweet length) to the database

# Imports
import tweepy
import sys
import mysql.connector
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#import Engine

# Global Variables
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="tweets"
)
new_fetch_ids = []
tweets=[]
userid=[]
tweetid=[]
faviourite=[]
retweet=[]
length=[]
cTweets=[]
# Constants
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


# Functions
def main_fetch(keyword, number_of_tweets):
    auth = tweepy.OAuthHandler('wV0igwcTKr8TjzJMwrM9dnl3P', 'D73364MRgWtyDXdkExN8EqfqvUFbjpV3fTAG0EjNqTBwcH59Dt')
    auth.set_access_token('1196832104342007809-AxxV7Zf4kvsvGAx0idjDqTVrRCWudT',
                          'UCtzmd9qtGY5zxEX65hgRHx5619SIiUA2SyAoMvUVLTe8')

    api = tweepy.API(auth, wait_on_rate_limit=True)
    for tweet in tweepy.Cursor(api.search, q=str(keyword), lang="en").items(int(number_of_tweets)):
        if tweet=='':
            print("No avilable tweets")
            sys.exit()
        tweets.append(tweet.text)
        userid.append(tweet.user.id)
        tweetid.append(tweet.id)
        faviourite.append(tweet.favorite_count)
        retweet.append(tweet.retweet_count)
        length.append(len(tweet.text))
    for i in range(len(tweets)):
        cTweets.append(tweets[i].replace('"',''))
        cursor = mydb.cursor()
        # cursor.execute(f"""DELETE FROM phrasecrediabilityoutput """)
        # mydb.commit()
        # cursor.execute(f"""DELETE FROM preprocessorr """)
        # mydb.commit()
        # cursor.execute(f"""DELETE FROM tweets """)
        # mydb.commit()
    for i in range(len(tweets)):
        cursor = mydb.cursor()
        cursor.execute(f"""INSERT INTO tweets (tweet, UserID, TweetID, FavouriteCount, RetweetCount, TweetLength) VALUES (" {cTweets[i]} ",{userid[i]},{tweetid[i]},{faviourite[i]},{retweet[i]},{length[i]}) """)
        new_fetch_ids.append(cursor.lastrowid)
        mydb.commit()
    # for n in new_fetch_ids:
    #     print(n)
    #     sql_select_Query = """SELECT ID FROM tweets WHERE tweet=%s """
    #     cursor = mydb.cursor()
    #     cursor.execute(sql_select_Query, (f""" " {cTweets[i]} " """,))
    #     myresult = cursor.fetchall()
    #     print(myresult)
    #     for x in myresult:
    #         print(x)
    #         new_fetch_ids.append(x[0][0])
    # for n in new_fetch_ids:
    #     print(n)
def clean_tweet(tweet):
    output_tweet = []
    filtered_sentence = []
    x = ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())
    stop_words = set(stopwords.words('english'))
    # tokens of words
    word_tokens = word_tokenize(x)
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    output_tweet.append(" ".join(filtered_sentence))
    return output_tweet[0]


def distribute_preprocessor():
    cursor = mydb.cursor()
    cursor.execute(f"""DELETE FROM preprocessorr """)
    mydb.commit()
    sql_select_query = """SELECT tweet FROM tweets WHERE ID=%s """
    for i in new_fetch_ids:
        cursor.execute(sql_select_query, (i,))
        tweet_raw = cursor.fetchall()

        cleaned_tweet = clean_tweet(tweet_raw[0][0])
        cursor.execute(f"""INSERT INTO preprocessorr (TweetID, PreProcessedData) VALUES ({i},"{cleaned_tweet}") """)
        mydb.commit()


# if __name__ == '__main__':
#     keyword = "trump"
#     number_of_tweets = 7
#     main_fetch(Eng, number_of_tweets)
    #distribute_preprocessor()