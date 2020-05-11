#imports
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt

# Global Variables
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="tweets"
)
phrase=[]
sentiment=[]
tweetsFeatures=[]
ps = []
percentage = []
barss = []
pp=[]
tweetID=[]
labels=[]
sentimentID=[]
phraseID=[]
tweetsFeaturesID=[]
news=[]
def weight():
    sql_select_Query = """SELECT TweetID,Label FROM phraseoutput ORDER BY ID ASC """
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query, )
    fetch = cursor.fetchall()
    for o in fetch:
        phrase.append(o[1])
        tweetID.append(o[0])
        # print("tweetID",o[1])
    sql_select_Query = """SELECT ID,Label FROM sentimentoutput ORDER BY ID ASC  """
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query, )
    fetch = cursor.fetchall()
    for o in fetch:
        sentiment.append(o[1])
        # print("sentiment label",o[0])
    sql_select_Query = """SELECT ID,Label FROM tweetfeaturesoutput ORDER BY ID ASC  """
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query, )
    fetch = cursor.fetchall()
    for o in fetch:
        tweetsFeatures.append(o[1])
        tweetsFeaturesID.append(o[0])
        # print("tweetfeatureID",o[1])
    sql_select_Query = """SELECT ID, Label FROM newsresults ORDER BY ID ASC  """
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query, )
    fetch = cursor.fetchall()
    for o in fetch:
        news.append(o[1])

    for i in range(len(tweetsFeatures)):

        pp.append((0.5*tweetsFeatures[i])+(0*sentiment[i])+(1*phrase[i])+(1.5*news[i]))
        # print("tweet",tweetsFeatures[i])
        # print("sentimnt", sentiment[i])
        # print("phrase", phrase[i]7
        # print(pp)
def prediaction():
    m=0
    for i in pp:
        #print(i)
        # if i>=1.5:
        #     ps.append(1).5
        # else:
        #     ps.append(0)
        percentage.append((i/3) * 100)
        m=m+1
        barss.append(m)
    cursor = mydb.cursor()
    cursor.execute(f"""DELETE FROM output """)
    mydb.commit()
    for i in range(len(percentage)):
        #print(percentage[i]+barss[i])
        cursor.execute(f"""INSERT INTO output (Percentage, TweetID,NumberOfTweets) VALUES ({percentage[i]},{tweetID[i]},{barss[i]}) """)
        mydb.commit()
        if percentage[i]>=66:
            labels.append(1)
        else:
            labels.append(0)
    #
    # for i in range(len(labels)):
    #
    #     cursor.execute(f"""INSERT INTO sentiment (TweetID, Result) VALUES ({tweetID[i]},{sentiment[i]}) """)
    #     mydb.commit()
        sql_select_Query = """SELECT ID FROM sentiment WHERE TweetID=%s """
        cursor = mydb.cursor()
        cursor.execute(sql_select_Query,(tweetID[i],) )
        fetch = cursor.fetchall()
        for o in fetch:
            sentimentID.append(o[0])
            # print("sentimentID",o[0])
        ##################################################
        # cursor.execute(f"""INSERT INTO phrasecrediabilityoutput (TweetID, Prediction) VALUES ({tweetID[i]},{phrase[i]}) """)
        # mydb.commit()
        sql_select_Query = """SELECT ID FROM phrasecrediabilityoutput WHERE TweetID=%s """
        cursor = mydb.cursor()
        cursor.execute(sql_select_Query, (tweetID[i],))
        fetch = cursor.fetchall()
        for o in fetch:
            phraseID.append(o[0])
            # print("phraseID",o[0])
            # print(labels[i])
        ##################################################
        cursor.execute(f"""INSERT INTO prediction (TweetID, SentimentID,PhraseCrediabilityID,Label) VALUES ({tweetID[i]},{sentimentID[i]},{phraseID[i]},{labels[i]}) """)
        mydb.commit()
        # print("tweetID",tweetID[i],"sentimentID",sentimentID[i],"phraseID",phraseID[i],"tweetFeatureID",tweetsFeaturesID[i])
# if __name__ == '__main__':
#     weight()
#     prediaction()
    #print("finally")