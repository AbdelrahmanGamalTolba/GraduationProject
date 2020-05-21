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
from sklearn import tree
from sklearn.model_selection import train_test_split
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
cont=[]
name = []
followers = []
friends = []
listed = []
favourite = []
status = []

nameee = []
followersss = []
friendsss = []
listeddd = []
favouriteee = []
statusss = []
clff = tree.DecisionTreeClassifier()
predict = []




# Functions
def usergraph():
    info = []
    label = []
    cursor = mydb.cursor()
    sql_select_Query = """SELECT screen_name, followers_count, friends_count, favourites_count, listed_count, statuses_count FROM userdataset """
    #cursor = mydb.cursor()
    cursor.execute(sql_select_Query, )
    fetchTweet = cursor.fetchall()
    for i in range(len(fetchTweet)):
        name.append(fetchTweet[i][0])
        followers.append(fetchTweet[i][1])
        friends.append(fetchTweet[i][2])
        favourite.append(fetchTweet[i][3])
        listed.append(fetchTweet[i][4])
        status.append(fetchTweet[i][5])
    for u in range(len(name)):
        # print(name[u])
        # print(followers[u])
        # print(friends[u])
        # print(favourite[u])
        # print(listed[u])
        # print(status[u])
        info.append([followers[u], friends[u], favourite[u], listed[u], status[u]])
    # for o in range(len(info)):
    #     print(info[o])
    sql_select_Query = """SELECT  Label FROM userdatasetoutput """
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query, )
    fetchTweet = cursor.fetchall()
    for i in range(len(fetchTweet)):
        label.append(fetchTweet[i][0])
    # for o in range(len(label)):
    #     print(label[o])
    # train_data = pd.read_csv('training_data_2_csv_UTF.csv')
    # train_attr = train_data[['id','screen_name','location','description','url','followers_count', 'friends_count', 'listed_count','created_at','favourites_count','verified','statuses_count', 'lang','default_profile','default_profile_image','has_extended_profile','name']]

    # train_attr = train_data[['followers_count', 'friends_count', 'listed_count','favourites_count','statuses_count']]
    # train_label = train_data[['bot']]

    # for k in range(len(followersss)):
    #     cursor = mydb.cursor()
    #     cursor.execute(
    #         f"""INSERT INTO userdataset (screen_name, followers_count, friends_count, favourites_count, listed_count, statuses_count) VALUES (" {nameee[k]} ",{followersss[k]},{friendsss[k]},{favouriteee[k]},{listeddd[k]},{statusss[k]}) """)
    #     new_fetch_ids.append(cursor.lastrowid)
    #     mydb.commit()
    #     predict.append([followersss[k], friendsss[k], favouriteee[k], listeddd[k], statusss[k]])
    data_train, data_test, labels_train, labels_test = train_test_split(info, label, test_size=0.3, random_state=0)

    clff.fit(data_train, labels_train)

def main_fetch(keyword, number_of_tweets):
    auth = tweepy.OAuthHandler('wV0igwcTKr8TjzJMwrM9dnl3P', 'D73364MRgWtyDXdkExN8EqfqvUFbjpV3fTAG0EjNqTBwcH59Dt')
    auth.set_access_token('1196832104342007809-AxxV7Zf4kvsvGAx0idjDqTVrRCWudT',
                          'UCtzmd9qtGY5zxEX65hgRHx5619SIiUA2SyAoMvUVLTe8')
    api = tweepy.API(auth, wait_on_rate_limit=True)

    for tweet in tweepy.Cursor(api.search, q=str(keyword+ " -filter:retweets"), lang="en").items(int(number_of_tweets)):

        predict.append([tweet.user.followers_count, tweet.user.friends_count, tweet.user.favourites_count, tweet.user.listed_count,tweet.user.statuses_count])
        predictions = clff.predict(predict)
        predict.pop()

        #print(tweet.text)
        #print(predictions)
        for r in userid:
            if r==tweet.user.id:
                for p in range(len(predictions)):
                    predictions[p]=0
                    #p=0
                #print("dfghjkl")
        for i in predictions:
            if i==1:
                #print(tweet.user.screen_name)
       # print("pred iteration",i)
                tweets.append(tweet.text)
                userid.append(tweet.user.id)
                tweetid.append(tweet.id)
                faviourite.append(tweet.favorite_count)
                retweet.append(tweet.retweet_count)
                length.append(len(tweet.text))

        # print(tweet.user.followers_count)
        # print(tweet.user.friends_count)
        # print(tweet.user.favourites_count)
        # print(tweet.user.listed_count)
        # print(tweet.user.statuses_count)
        # print("old",userid)
    #for t in range(number_of_tweets):

    validation(keyword,number_of_tweets)
    for i in range(len(tweets)):
        cTweets.append(tweets[i].replace('"',''))
        # cursor = mydb.cursor()
        # cursor.execute(f"""DELETE FROM phrasecrediabilityoutput """)
        # mydb.commit()
        # cursor.execute(f"""DELETE FROM preprocessorr """)
        # mydb.commit()
        # cursor.execute(f"""DELETE FROM tweets """)
        # mydb.commit()
    # for i in range(len(tweets)):
    #
    #     print(cTweets[i],userid[i],tweetid[i],faviourite[i],retweet[i],length[i])
        # cursor = mydb.cursor()
        # cursor.execute(f"""INSERT INTO tweets (tweet, UserID, TweetID, FavouriteCount, RetweetCount, TweetLength) VALUES (" {cTweets[i]} ",{userid[i]},{tweetid[i]},{faviourite[i]},{retweet[i]},{length[i]}) """)
        # new_fetch_ids.append(cursor.lastrowid)
        # mydb.commit()

def validation(keyword,number_of_tweets):
    if len(userid) < int(number_of_tweets):
        new = int(number_of_tweets) - len(userid)
        #print("new", new)
        main_fetch(keyword, new)


def sql():
    for i in range(len(tweets)):
        #print(i)
        cursor = mydb.cursor()
        cursor.execute(f"""INSERT INTO tweets (tweet, UserID, TweetID, FavouriteCount, RetweetCount, TweetLength) VALUES (" {cTweets[i]} ",{userid[i]},{tweetid[i]},{faviourite[i]},{retweet[i]},{length[i]}) """)
        new_fetch_ids.append(cursor.lastrowid)
        mydb.commit()
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
        #print(cleaned_tweet)
        cursor.execute(f"""INSERT INTO preprocessorr (TweetID, PreProcessedData) VALUES ({i},"{cleaned_tweet}") """)
        mydb.commit()


# if __name__ == '__main__':
#     keyword = "Taylor Swift cancels all appearances"
#     number_of_tweets = 7
#     usergraph()
#     main_fetch(keyword, number_of_tweets)
#     sql()
#     distribute_preprocessor()