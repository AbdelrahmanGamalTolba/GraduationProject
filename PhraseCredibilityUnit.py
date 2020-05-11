#imports
import pandas as pd
import mysql.connector
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import tree, svm
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import  VotingClassifier

# Global Variables
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="tweets"
)
def main_function():
    text=[]
    label=[]
    cleanText=[]
    Tweetid=[]
    cursor = mydb.cursor()
    sql_select_query = """SELECT Tweet,Label FROM phrasecrediabilitydataset  """
    cursor.execute(sql_select_query)
    tweet_raw = cursor.fetchall()
    for i in tweet_raw:
        text.append(i[0])
        label.append(i[1])
    data_train, data_test, labels_train, labels_test = train_test_split(text, label,test_size=0.3,random_state=0)
   # print(tweet_raw)
#
#print("data_train, labels_train : ",data_train.shape, labels_train.shape)

#spam,Camera - You are awarded a SiPix Digital Camera! call 09061221066 fromm landline. Delivery within 28 days
    vectorizer = CountVectorizer()

    data_train_count = vectorizer.fit_transform(data_train)
    data_test_count  = vectorizer.transform(data_test)



    from sklearn import tree, svm

    clff = svm.SVC(kernel='linear', C = 1)
    clff.fit(data_train_count, labels_train)
    predictions = clff.predict(data_test_count)
#print("accuracy_score : ", accuracy_score(labels_test, predictions)*100)


    #raw = pd.read_csv('cleanTweets.csv',encoding='latin-1')
#csvFilee2 = open('tweettestprediction.csv', 'w',newline="")
#csvWriterr2 = csv.writer(csvFilee2)
    #tt=raw["text"]
    sql_select_query = """SELECT TweetID,PreProcessedData FROM preprocessorr  """
    cursor.execute(sql_select_query)
    clean_tweet_raw = cursor.fetchall()
    for i in clean_tweet_raw:
        cleanText.append(i[1])
        Tweetid.append(i[0])
        data_trainn = vectorizer.transform(cleanText)

        textpp = clff.predict(data_trainn)
    #print(textpp)
    # cursor.execute(f"""DELETE FROM phrasecrediabilityoutput """)
    # mydb.commit()
    for u in range(len(textpp)):
        cursor.execute(f"""INSERT INTO phrasecrediabilityoutput (TweetID, Prediction) VALUES ("{Tweetid[u]}",{textpp[u]}) """)
        mydb.commit()
    #for u in textpp:
    #csvWriterr2.writerow([u])
    #print(u)
def phrase_output(Category):
    category=Category
    new_fetch_ids=[]
    finalResult=[]
    result=[]
    labels=[]
    phrase=[]
    newfetchTweet=[]
    train=[]
    percentageAccuracy=[]
    predict=[]
    newPhraseResult=[]
    cleantext=[]
    ###########################################################################
    # sql_select_Query = """SELECT TweetID,Label FROM prediction  """
    # cursor = mydb.cursor()
    # cursor.execute(sql_select_Query,)
    # myresult = cursor.fetchall()
    # for i in myresult:
    #     new_fetch_ids.append(i[0])
    #     labels.append(i[1])
    ##############################################################################


    cursor = mydb.cursor()
    sql_select_query = """SELECT PreProcessedData FROM preprocessorr  """
    cursor.execute(sql_select_query)
    clean_tweet_raw = cursor.fetchall()
    for i in clean_tweet_raw:
        cleantext.append(i[0])
        #Tweetid.append(i[0])
        vectorizer = CountVectorizer()

        #data_trainn = vectorizer.transform(cleantext)

        #textpp = clff.predict(data_trainn)







    # #for i in range(len(new_fetch_ids)):
    # sql_select_Query = """SELECT Tweet,Label FROM phrasecrediabilitydataset  """
    # cursor = mydb.cursor()
    # cursor.execute(sql_select_Query)
    # myresulttt = cursor.fetchall()
    #
    # for i in myresulttt:
    #     phrase.append(i[0])
    #     labels.append(i[1])
    # for u in range(len(phrase)):
    #     train.append([phrase[u]])
###############################################################################################
    if category=='Celebrity':
        print("c")
        sql_select_Query = """SELECT Text,Label FROM celebritydataset"""
        cursor = mydb.cursor()
        cursor.execute(sql_select_Query)
        myresulttt = cursor.fetchall()

        for i in myresulttt:
            phrase.append(i[0])
            labels.append(i[1])
        for u in range(len(phrase)):
            train.append([phrase[u]])
        ########################################################################################
        sql_select_Query = """SELECT Text,Label FROM gossipdataset  """
        cursor = mydb.cursor()
        cursor.execute(sql_select_Query)
        myresulttt = cursor.fetchall()
        for i in myresulttt:
            phrase.append(i[0])
            labels.append(i[1])
        for u in range(len(phrase)):
            train.append([phrase[u]])
    ###############################################################################################
    if category=='Politics':
    #     print("p")
    #     sql_select_Query = """SELECT Text,Label FROM politicsdataset"""
    #     cursor = mydb.cursor()
    #     cursor.execute(sql_select_Query)
    #     myresulttt = cursor.fetchall()
    #     for i in myresulttt:
    #         phrase.append(i[0])
    #         labels.append(i[1])
    #     for u in range(len(phrase)):
    #         train.append([phrase[u]])
    #         #print(phrase[u])
    #############################################################################################
        sql_select_Query = """SELECT Text,Label FROM dataset3  """
        cursor = mydb.cursor()
        cursor.execute(sql_select_Query)
        myresulttt = cursor.fetchall()
        for i in myresulttt:
            phrase.append(i[0])
            labels.append(i[1])
        for u in range(len(phrase)):
            train.append([phrase[u]])
##########################################################################################
    # sql_select_Query = """SELECT Text,Label FROM dataset4  """
    # cursor = mydb.cursor()
    # cursor.execute(sql_select_Query)
    # myresulttt = cursor.fetchall()
    # for i in myresulttt:
    #     phrase.append(i[0])
    #     labels.append(i[1])
    # for u in range(len(phrase)):
    #     train.append([phrase[u]])
########################################################################################
    # sql_select_Query = """SELECT Text,Label FROM politicsdataset  """
    # cursor = mydb.cursor()
    # cursor.execute(sql_select_Query)
    # myresulttt = cursor.fetchall()
    # for i in myresulttt:
    #     phrase.append(i[0])
    #     labels.append(i[1])
    # for u in range(len(phrase)):
    #     train.append([phrase[u]])



    sql_select_Query = """SELECT TweetID FROM preprocessorr"""
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    fetchTweet = cursor.fetchall()
    for i in range(len(fetchTweet)):
        newfetchTweet.append(fetchTweet[i][0])

    # for i in range(len(newfetchTweet)):
    #     sql_select_Query = """SELECT Prediction FROM phrasecrediabilityoutput WHERE TweetID=%s """
    #     cursor = mydb.cursor()
    #     cursor.execute(sql_select_Query, (newfetchTweet[i],))
    #     fetchTweet = cursor.fetchall()
    #     for i in range(len(fetchTweet)):
    #         newPhraseResult.append(fetchTweet[i][0])
    # for u in range(len(newPhraseResult)):
    #     predict.append([newPhraseResult[u]])
    #prnt(len(sentiment))
    data_train, data_test, labels_train, labels_test = train_test_split(phrase, labels, test_size=0.3,random_state=0)
    ###################Decisiontree######################
    clff = tree.DecisionTreeClassifier()
    #clff = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes = (5, 2), random_state = 1)
    #####mohm vectorizer = CountVectorizer()
    #####mohm data_train_count = vectorizer.fit_transform(data_train)
    #####mohm data_test_count = vectorizer.transform(data_test)
    #####mohm clff.fit(data_train_count, labels_train)
    #####mohm  data_trainn = vectorizer.transform(cleantext)
    # predictions = clff.predict(data_test_count)
    # print(accuracy_score(labels_test,predictions)*100)
    #####mohm  predictionsDT = clff.predict(data_trainn)
    # print(predictionsDT)
    ###################NeuralNetwork######################
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes = (5, 2), random_state = 1)
    #####mohm vectorizer = CountVectorizer()
    #####mohm data_train_count = vectorizer.fit_transform(data_train)
    #####mohm data_test_count = vectorizer.transform(data_test)
    #####mohm clf.fit(data_train_count, labels_train)
    #####mohm   data_trainn = vectorizer.transform(cleantext)
    # predictions = clff.predict(data_test_count)
    # print(accuracy_score(labels_test,predictions)*100)
    #####mohm   predictionsNN = clf.predict(data_trainn)
    # print(predictionsNN)
    ###################SVM######################
    clfSVM = svm.SVC(kernel='linear', C = 1)
    #####mohm    vectorizer = CountVectorizer()
    #####mohm    data_train_count = vectorizer.fit_transform(data_train)
    #####mohm    data_test_count = vectorizer.transform(data_test)
    #####mohm  clfSVM.fit(data_train_count, labels_train)
    #####mohm  data_trainn = vectorizer.transform(cleantext)
    # predictions = clff.predict(data_test_count)
    # print(accuracy_score(labels_test,predictions)*100)
   #####mohm predictionsSVM = clfSVM.predict(data_trainn)
    # print(predictionsSVM)
    # cursor.execute(f"""DELETE FROM phraseoutput """)
    # mydb.commit()
    # for i in range(len(predictions)):
    #     cursor.execute(f"""INSERT INTO phraseoutput (TweetID, Label) VALUES ({newfetchTweet[i]},{predictions[i]}) """)
    #     mydb.commit()
    eclf1 = VotingClassifier(estimators=[('DecissionTree', clff), ('NN', clf), ('svm', clfSVM)], voting='hard')
    vectorizer = CountVectorizer()
    data_train_count = vectorizer.fit_transform(data_train)
    data_test_count = vectorizer.transform(data_test)
    eclf1.fit(data_train_count, labels_train)
    #eclf1.fit(data_train, labels_train)
    data_trainn = vectorizer.transform(cleantext)

    VotingPred = eclf1.predict(data_trainn)
    #print(VotingPred)
    for i in VotingPred:
        percentageAccuracy.append(i)
    # print(VotingPred)
    # for i in range(len(predictionsSVM)):
    #     result.append((0.2*int(predictionsDT[i]))+(0.3*int(predictionsNN[i]))+(0.5*int(predictionsSVM[i])))
    # for i in result:
    #     finalResult.append((i) * 100)
    # for i in finalResult:
    #     if i>=50 :
    #         percentageAccuracy.append(1)
    #     else:
    #         percentageAccuracy.append(0)
    #print(percentageAccuracy)
    cursor.execute(f"""DELETE FROM phraseoutput """)
    mydb.commit()
    for i in range(len(percentageAccuracy)):
        cursor.execute(f"""INSERT INTO phraseoutput (TweetID, Label) VALUES ({newfetchTweet[i]},{percentageAccuracy[i]}) """)
        mydb.commit()
# if __name__ == '__main__':
#      #main_function()
#     cc="Celebrity"
#     pp="Politics"
#     phrase_output(pp)
