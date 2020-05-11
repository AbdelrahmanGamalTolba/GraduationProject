# Imports
import os
import sys
import FetchUnit
import TweetFeaturesClassifierUnit
import SentimentAnalysisUnit
import PhraseCredibilityUnit
import PredictionUnit
import bbc
keyword =sys.argv[1]
number_of_tweets =sys.argv[2]
category=sys.argv[3]
# Run Fetch Unit
#os.system('C:/xamppp/htdocs/twitterapi/venv\Scripts/activate && cd C:/Users/hp/Desktop/twitterapi && python C:/xamppp\htdocs/twitterapi\Engine.py"'+keyword+'" "'+number_of_tweets+'"')
##os.system(f"""C:/xamppp/htdocs/twitterapi/venv/Scripts/activate && cd C:/Users/hp/Desktop/twitterapi && python C:/xamppp/htdocs/twitterapi/FetchUnit.py  """)
FetchUnit.main_fetch(keyword,number_of_tweets)
FetchUnit.distribute_preprocessor()
# Run Phrase Credibility Unit
##os.system(f"""C:/xamppp/htdocs/twitterapi/venv/Scripts/activate && cd C:/Users/hp/Desktop/twitterapi && python C:/xamppp/htdocs/twitterapi/PhraseCredibilityUnit.py """)
PhraseCredibilityUnit.main_function()
PhraseCredibilityUnit.phrase_output(category)
# Run Tweet Features Classifier Unit
#os.system(f"""C:/xamppp/htdocs/twitterapi/venv/Scripts/activate && cd C:/Users/hp/Desktop/twitterapi && python C:/xamppp/htdocs/twitterapi/TweetFeaturesClassifierUnit.py """)
TweetFeaturesClassifierUnit.main_function()
# Run Sentiment Analysis Unit
##os.system(f"""C:/xamppp/htdocs/twitterapi/venv/Scripts/activate && cd C:/Users/hp/Desktop/twitterapi && python C:/xamppp/htdocs/twitterapi/SentimentAnalysisUnit.py """)
SentimentAnalysisUnit.main_sentiment()
SentimentAnalysisUnit.sentiment_output()
#check news API
bbc.getKey(keyword)
# Run Prediction Unit
##os.system(f"""C:/xamppp/htdocs/twitterapi/venv/Scripts/activate && cd C:/Users/hp/Desktop/twitterapi && python C:/xamppp/htdocs/twitterapi/PredictionUnit.py """)
PredictionUnit.weight()
PredictionUnit.prediaction()
