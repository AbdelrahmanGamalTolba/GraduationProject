#imports
from textblob import TextBlob
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn import tree
# Global Variables
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="tweets"
)
def main_sentiment():
    sql_select_Query = """SELECT TweetID,PreProcessedData FROM preprocessorr  """
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    myresult = cursor.fetchall()
    # cursor.execute(f"""DELETE FROM sentiment """)
    # mydb.commit()
    for i in myresult:
        sentiment_result = analyze_sentiment(i[1])
        cursor.execute(f"""INSERT INTO sentiment (TweetID, Result) VALUES ({i[0]},"{sentiment_result}") """)
        mydb.commit()

def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 1
    # if analysis.sentiment.polarity == 0:
    #     return 2
    else:
        return 0

def sentiment_output():
    new_fetch_ids=[]
    labels=[]
    sentiment=[]
    newfetchTweet=[]
    train=[]
    predict=[]
    newSentimentResult=[]
    ##########################################################################
    # sql_select_Query = """SELECT TweetID,Label FROM prediction  """
    # cursor = mydb.cursor()
    # cursor.execute(sql_select_Query,)
    # myresult = cursor.fetchall()
    # for i in myresult:
    #     new_fetch_ids.append(i[0])
    #     labels.append(i[1])
    ############################################################################
    sql_select_Query = """SELECT Sentiment,FinalLabel FROM dataset  """
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    myresulttt = cursor.fetchall()
    for i in myresulttt:
        sentiment.append(i[0])
        labels.append([i[1]])

    for u in range(len(sentiment)):
        train.append([sentiment[u]])
    sql_select_Query = """SELECT TweetID FROM preprocessorr"""
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    fetchTweet = cursor.fetchall()
    for i in range(len(fetchTweet)):
        newfetchTweet.append(fetchTweet[i][0])

    for i in range(len(newfetchTweet)):
        sql_select_Query = """SELECT Result FROM sentiment WHERE TweetID=%s """
        cursor = mydb.cursor()
        cursor.execute(sql_select_Query, (newfetchTweet[i],))
        fetchTweet = cursor.fetchall()
        for i in range(len(fetchTweet)):
            newSentimentResult.append(fetchTweet[i][0])
    for u in range(len(newSentimentResult)):
        predict.append([newSentimentResult[u]])
    #prnt(len(sentiment))
    data_train, data_test, labels_train, labels_test = train_test_split(train, labels, random_state=0)
    # clff = svm.SVC(kernel='linear', C = 1)
    # print(train)
    # print("labels",labels)
    # print("pred",predict)
    clff = tree.DecisionTreeClassifier()
    clff.fit(data_train, labels_train)
    predictions = clff.predict(predict)
    # print(predict)
    #print(predictions)
    cursor.execute(f"""DELETE FROM sentimentoutput """)
    mydb.commit()
    for i in range(len(predict)):
        cursor.execute(f"""INSERT INTO sentimentoutput (TweetID, Label) VALUES ({newfetchTweet[i]},{predict[i][0]}) """)
        mydb.commit()
# if __name__ == '__main__':
# #     main_sentiment()
#     sentiment_output()