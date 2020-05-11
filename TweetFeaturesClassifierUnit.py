#imports
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn import tree, svm
from sklearn.metrics import accuracy_score
from sklearn.ensemble import  VotingClassifier


# Global Variables
from sklearn.neural_network import MLPClassifier

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="tweets"
)

def main_function():
    new_fetch_ids = []
    labels = []
    sentiment = []
    phrase = []
    text=[]
    retweet = []
    favourite = []
    length = []
    newtext=[]
    newretweet = []
    newfavourite = []
    newlength = []
    newfetchTweet = []
    Tweetid=[]
    newSentimentID = []
    newphraseID = []
    train = []
    predict=[]
    result=[]
    percentageAccuracy=[]
    finalResult=[]
    predictionsSVM=[]
    predictionsDT=[]
    # raw = pd.read_csv('XX.csv',encoding='latin-1')
    # trainT = raw[['retweet_count','favorite_count','length','Sentiment','prediction']]
    # labelT=raw['FinalLabel']
    ######################################################################################
    # sql_select_Query = """SELECT TweetID,Label FROM prediction  """
    # cursor = mydb.cursor()
    # cursor.execute(sql_select_Query, )
    # myresult = cursor.fetchall()
    # for i in myresult:
    #     new_fetch_ids.append(i[0])
    #     labels.append(i[1])
    ######################################################################################
    # for i in range(len(new_fetch_ids)):
        # print("id kol haga labeled",new_fetch_ids[i])
    sql_select_Query = """SELECT retweet_count,favorite_count,length, FinalLabel FROM dataset   """
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    myresultTweet = cursor.fetchall()
    for o in myresultTweet:
        #print(o)
        #text.append(o[0])
        retweet.append(o[0])
        favourite.append(o[1])
        length.append(o[2])
        labels.append(o[3])
    for u in range(len(favourite)):
        train.append([retweet[u], favourite[u], length[u]])

#############################################################
    # sql_select_Query = """SELECT ID FROM tweets"""
    # cursor = mydb.cursor()
    # cursor.execute(sql_select_Query)
    # fetchTweet = cursor.fetchall()
    # for i in range(len(fetchTweet)):
    #     # print(fetchTweet[i])
    #     newfetchTweet.append(fetchTweet[i][0])
    # for u in new_fetch_ids:
    #     # print("id kol haga",u)
    #     if u in newfetchTweet:
    #         newfetchTweet.remove(u)
    # print(len(newfetchTweet))
    # print(newfetchTweet)
    ##############################################################3
    # for k in range(len(newfetchTweet)):
        # print("id el gded bs ",newfetchTweet[k])
    sql_select_Query = """SELECT TweetID FROM preprocessorr"""
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    fetchTweet = cursor.fetchall()
    for i in range(len(fetchTweet)):
        Tweetid.append(fetchTweet[i][0])

    for i in range(len(Tweetid)):
        sql_select_Query = """SELECT ID ,FavouriteCount,RetweetCount,TweetLength FROM tweets WHERE ID=%s  """
        cursor = mydb.cursor()
        #print(Tweetid[i])
        cursor.execute(sql_select_Query, (Tweetid[i],))
        myresultTweet = cursor.fetchall()
        #print(myresultTweet)
        for o in myresultTweet:
        #print(o[0])
            newfetchTweet.append(o[0])
            newfavourite.append(o[1])
            newretweet.append(o[2])
            newlength.append(o[3])
    cursor = mydb.cursor()
    sql_select_query = """SELECT PreProcessedData FROM preprocessorr  """
    cursor.execute(sql_select_query)
    clean_tweet_raw = cursor.fetchall()
    for i in clean_tweet_raw:
        newtext.append(i[0])
    #print(len(newfavourite))
    for u in range(len(newfavourite)):
        predict.append([newretweet[u], newfavourite[u], newlength[u]])
    #print(train)
    data_train, data_test, labels_train, labels_test = train_test_split(train,labels,random_state=0)
    #clff = svm.SVC(kernel='linear', C = 1)
    #clff=tree.DecisionTreeClassifier()
    #clff = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes = (5, 2), random_state = 1)

    #clff.fit(data_train, labels_train)
    #predictions = clff.predict(predict)
    # print(predict)
    # print(predictions)

    ###################Decisiontree######################
    clff = tree.DecisionTreeClassifier()
    # clff = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes = (5, 2), random_state = 1)
    #clff.fit(data_train, labels_train)
    # predictions = clff.predict(data_test_count)
    # print(accuracy_score(labels_test,predictions)*100)
   # predictionsDT = clff.predict(predict)
        # print(predictionsDT)
    ###################NeuralNetwork######################
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
   # clf.fit(data_train, labels_train)
    # predictions = clff.predict(data_test_count)
    # print(accuracy_score(labels_test,predictions)*100)
#    predictionsNN = clf.predict(predict)
    # print(predictionsNN)
    ###################NeuralNetwork######################
    clfSVM = svm.SVC(kernel='linear', C=1)
    #clfSVM.fit(data_train, labels_train)
    eclf1 = VotingClassifier(estimators=[('DecissionTree', clff), ('NN', clf), ('svm', clfSVM)], voting='hard')
    eclf1.fit(data_train, labels_train)

    # predictions = clff.predict(data_test_count)
    # print(accuracy_score(labels_test,predictions)*100)
    #predictionsSVM = clfSVM.predict(predict)
    # print(predictionsSVM)
    # cursor.execute(f"""DELETE FROM phraseoutput """)
    # mydb.commit()
    # for i in range(len(predictions)):
    #     cursor.execute(f"""INSERT INTO phraseoutput (TweetID, Label) VALUES ({newfetchTweet[i]},{predictions[i]}) """)
    #     mydb.commit()

    VotingPred = eclf1.predict(predict)
    for i in VotingPred:
        percentageAccuracy.append(i)
    print(VotingPred)

    # for i in range(len(predictionsSVM)):
    #     result.append((0.2 * predictionsDT[i]) + (0.3 * predictionsNN[i]) + (0.5 * predictionsSVM[i]))
    # for i in result:
    #     finalResult.append((i) * 100)
    # for i in finalResult:
    #     if i >= 50:
    #         percentageAccuracy.append(1)
    #     else:
    #         percentageAccuracy.append(0)
    # print(percentageAccuracy)
    #
    cursor.execute(f"""DELETE FROM tweetfeaturesoutput """)
    mydb.commit()
    for jj in range(len(percentageAccuracy)):
        cursor.execute(f"""INSERT INTO tweetfeaturesoutput (TweetID, Label) VALUES ({newfetchTweet[jj]},{percentageAccuracy[jj]})""")
        mydb.commit()

# if __name__ == '__main__':
#     main_function()