import requests
import json
import mysql.connector
import pandas as pd
import difflib
import paralleldots
import requests
import sys
# Global Variables
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="tweets"
)
tweetid=[]
tweets=[]
ratio=[]
J=[]
l1=[]
max_data=[]
label=[]
def getKey(keyword):



    cursor = mydb.cursor()
    sql_select_query = """SELECT PreProcessedData FROM preprocessorr  """
    cursor.execute(sql_select_query)
    clean_tweet_raw = cursor.fetchall()
    for i in clean_tweet_raw:
        tweets.append(i[0])

    cursor = mydb.cursor()
    sql_select_query = """SELECT TweetID FROM preprocessorr  """
    cursor.execute(sql_select_query)
    clean_tweet_raw = cursor.fetchall()
    for i in clean_tweet_raw:
        tweetid.append(i[0])

    # sql_select_query = """SELECT tweet FROM tweets WHERE ID=%s """
    # for i in tweetid:
    #     cursor.execute(sql_select_query, (i,))
    #     tweet_raw = cursor.fetchall()
    #     tweets = tweet_raw[0][0]
    #     #print(tweets)

    # The headers remain the same for all the requests
    ##############Abdo################################
    # headers = {'Authorization': 'b7de039e294740bb84d8dff8c2bbf97d'}
    #############Mariam################################
    headers = {'Authorization': '77e2da38fc504c82be37be69c564d820'}

    # All the endpoints in this section

    # To fetch the top headlines
    top_headlines_url = 'https://newsapi.org/v2/top-headlines'
    # To fetch news articles
    everything_news_url = 'https://newsapi.org/v2/everything'
    # To retrieve the sources
    sources_url = 'https://newsapi.org/v2/sources'

    # Add parameters to request URL based on what type of headlines news you want

    # All the payloads in this section
    headlines_payload = {'category': 'politics', 'country': 'us','pageSize': 100}
    everything_payload = {'q': str(keyword), 'language': 'en','pageSize': 100}
    sources_payload = {'category': 'general', 'language': 'en', 'country': 'us','pageSize': 100}

    # Fire a request based on the requirement, just change the url and the params field

    # Request to fetch the top headlines
    #response = requests.get(url=top_headlines_url, headers=headers, params=headlines_payload)

    # Request to fetch every news article
    response = requests.get(url=everything_news_url, headers=headers, params=everything_payload)
    #print(response.text)
    # Request to fetch the sources
    #response = requests.get(url=sources_url, headers=headers, params=sources_payload)

    # If you just want to print
    pretty_json_output = json.dumps(response.json())
   ######### print(pretty_json_output)
    # print(response.json())

    # To store the relevant json data to a csv

    # Convert response to a pure json string
    response_json_string = json.dumps(response.json())

    # A json object is equivalent to a dictionary in Python
    # retrieve json objects to a python dict
    response_dict = json.loads(response_json_string)
   ######### print(response_dict)

    # Info about articles is represented as an array in the json response
    # A json array is equivalent to a list in python
    # We want info only about articles
    articles_list = response_dict['articles']

    # We want info only about sources
    # sources_list = response_dict['sources']
    # And then you can specify one of these sources explicitly if you like while fetching the news

    # Convert articles list to json string , convert json string to dataframe , write df to csv!
    df = pd.read_json(json.dumps(articles_list))

    # Convert sources list to json string , convert json string to dataframe , write df to csv!
    # df = pandas.read_json(json.dumps(sources_list))

    # Using Pandas write the json data to a csv
    df.to_csv('C:\\xamppp\\htdocs\\twitterapi\\bbcnews8.csv')
    #print("x")
    url = "https://twinword-text-similarity-v1.p.rapidapi.com/similarity/"
    ###################Abdo#####################################
    # headerss = {
    #     'x-rapidapi-host': "twinword-text-similarity-v1.p.rapidapi.com",
    #     'x-rapidapi-key': "332699e504msh4ec476b6cf72862p12b8cdjsn33d9b8047991"
    # }
    ###################John#######################################
    # headerss = {
    #     'x-rapidapi-host': "twinword-text-similarity-v1.p.rapidapi.com",
    #     'x-rapidapi-key': "0d670421femsh7ea3286a8b8984ap1a9809jsn3e2b59ba7567"
    # }
    ###############Mariam########################################
    headerss = {
        'x-rapidapi-host': "twinword-text-similarity-v1.p.rapidapi.com",
        'x-rapidapi-key': "5f8b4354dbmshc0b724609c1ccdep1308f5jsn0f2ef08c39f5"
    }
    rawnews = pd.read_csv('C:\\xamppp\\htdocs\\twitterapi\\bbcnews8.csv',encoding='latin-1')
    train = rawnews['title']
    ratio=[]
    for i in range(len(tweets)):
        #print(i)
        for j in range(len(train)):
            querystring = {"text1": train[j],
                           "text2": tweets[i]}
            response = requests.request("GET", url, headers=headerss, params=querystring)

            ss = response.text

            s = ss.split(",")
            c = s[0].split(":")
            #print(c)
            ratio.append(float(c[1]))
            # ratio = paralleldots.similarity(train[j], tweets[i])
            # print(ratio)
            #ratio.append(difflib.SequenceMatcher(None, train[j], tweets[i]).ratio())
    divition=len(ratio)/len(tweets)
    print(divition)
    count=0
    for x in range(len(ratio)):

        if count < divition-1:
            l1.append(ratio[x])
            count+=1
            #print(count)
        else:
            res_max = max(float(sub) for sub in l1)
            #print(len(l1))
            max_data.append(res_max)
            l1.clear()
            count = 0
            l1.append(ratio[x])


    #print(max_data)
    for o in max_data:
        if o>0.5:
            label.append(1)
        else:
            label.append(0)
    #print(label)
        # print(ratio)
        # print("############")
    # for d in range(99):
    #     res_max = max(float(sub) for sub in ratio)
    # print(res_max)
        #print(ratio[d].float_info.max)
   # print(ratio.sort().float_info.max)
    #     for dd in range(99):
    #         if ratio[d]>ratio[dd]:
    #             max=ratio[d]
    #print(max)
        # J.append(ratio[d])
        # print(ratio[d])
        #print(max(ratio[d],ratio[d+1]))
    #print(len(train))
    cursor = mydb.cursor()
    cursor.execute(f"""DELETE FROM newsresults """)
    mydb.commit()
    for i in range(len(label)):
        print(label[i])
        cursor.execute(f"""INSERT INTO newsresults (TweetID, Label) VALUES ({tweetid[i]},{label[i]}) """)
        mydb.commit()
# if __name__ == '__main__':
#     getKey("Prince Charles tested positive for coronavirus")