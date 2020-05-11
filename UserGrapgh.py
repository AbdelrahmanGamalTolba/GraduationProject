#imports
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
import tweepy
import mysql.connector
import sys
import time
# Global Variables
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="tweets"
)
def main_function(x):
    access_token = "1196832104342007809-AxxV7Zf4kvsvGAx0idjDqTVrRCWudT"
    access_token_secret = "UCtzmd9qtGY5zxEX65hgRHx5619SIiUA2SyAoMvUVLTe8"
    consumer_key = "wV0igwcTKr8TjzJMwrM9dnl3P"
    consumer_secret = "D73364MRgWtyDXdkExN8EqfqvUFbjpV3fTAG0EjNqTBwcH59Dt"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    user = api.get_user(1196832104342007809)
    #print(user.screen_name)
    name = []
    followers = []
    friends = []
    listed = []
    favourite = []
    status = []
    nameee=[]
    followersss = []
    friendsss = []
    listeddd = []
    favouriteee = []
    statusss = []
    train_label = []
    info=[]
    label=[]
    predict=[]
    new_fetch_ids=[]
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=str(x), exclude_replies=True).items(1):
        # print(tweet.user.screen_name)
        # print(tweet.user.followers_count)
        # print(tweet.user.friends_count)
        # print(tweet.user.favourites_count)
        # print(tweet.user.listed_count)
        # print(tweet.user.statuses_count)
        nameee.append(tweet.user.screen_name)
        followersss.append(tweet.user.followers_count)
        friendsss.append(tweet.user.friends_count)
        favouriteee.append(tweet.user.favourites_count)
        listeddd.append(tweet.user.listed_count)
        statusss.append(tweet.user.statuses_count)
        #print(len(followersss))

    sql_select_Query = """SELECT screen_name, followers_count, friends_count, favourites_count, listed_count, statuses_count FROM userdataset """
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query,)
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
        info.append([followers[u],friends[u],favourite[u],listed[u],status[u]])
    # for o in range(len(info)):
    #     print(info[o])
    sql_select_Query = """SELECT  Label FROM userdatasetoutput """
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query,)
    fetchTweet = cursor.fetchall()
    for i in range(len(fetchTweet)):
        label.append(fetchTweet[i][0])
    # for o in range(len(label)):
    #     print(label[o])
    #train_data = pd.read_csv('training_data_2_csv_UTF.csv')
    # train_attr = train_data[['id','screen_name','location','description','url','followers_count', 'friends_count', 'listed_count','created_at','favourites_count','verified','statuses_count', 'lang','default_profile','default_profile_image','has_extended_profile','name']]

    # train_attr = train_data[['followers_count', 'friends_count', 'listed_count','favourites_count','statuses_count']]
    # train_label = train_data[['bot']]

    for k in range(len(followersss)):
        cursor = mydb.cursor()
        cursor.execute(f"""INSERT INTO userdataset (screen_name, followers_count, friends_count, favourites_count, listed_count, statuses_count) VALUES (" {nameee[k]} ",{followersss[k]},{friendsss[k]},{favouriteee[k]},{listeddd[k]},{statusss[k]}) """)
        new_fetch_ids.append(cursor.lastrowid)
        mydb.commit()
        predict.append([followersss[k],friendsss[k],favouriteee[k],listeddd[k],statusss[k]])
    data_train, data_test, labels_train, labels_test = train_test_split(info, label )
    clff = tree.DecisionTreeClassifier()
    clff.fit(data_train, labels_train)
    predictions = clff.predict(predict)
    #print(predictions)
    # clf_predictions = clff.predict(data_test)
    # print("Accuracy: {}%", accuracy_score(labels_test, clf_predictions)*100)
    cursor.execute(f"""DELETE FROM useroutput """)
    mydb.commit()
    cursor = mydb.cursor()
    cursor.execute(f"""INSERT INTO useroutput (UserID, Label) VALUES (" {new_fetch_ids[0]} ",{predictions[0]}) """)
    mydb.commit()
    cursor.execute(f"""INSERT INTO userdatasetoutput (UserDatasetID, Label) VALUES (" {new_fetch_ids[0]} ",{predictions[0]}) """)
    mydb.commit()
# if __name__ == '__main__':
#     username=sys.argv[1]
#     main_function(username)
