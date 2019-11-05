# this is the code for querying tweets from Twitter API
# time range: Sep 13 to Sep 19
# tweets with hashtag #taylorswift OR #TaylorSwift OR #Lover

'''
import tweepy
import time
from datetime import datetime
import json
import pandas as pd
import csv 
auth = tweepy.auth.OAuthHandler('SCRET', 'SECRET')
auth.set_access_token('SECRET', 'SECRET')

api = tweepy.API(auth)
   
count = 0

start = ["2019-09-13", "2019-09-14", "2019-09-15", "2019-09-16", "2019-09-17", "2019-09-18", "2019-09-19"]


with open('json_file1.json', 'a') as f:

	for i in range(len(start) - 1):

		try:

			for tweet in tweepy.Cursor(api.search, q = "#taylorswift OR TaylorSwift OR Lover", since = start[i], until = start[i+1], lang = "en").items(2000):
				#print(tweet.created_at)
				count += 1

				json.dump(tweet._json, f)
				f.write('\n')

		except tweepy.TweepError:
			time.sleep(1000)
'''

# save the data to a json file

import pandas as pd
import re
import emoji
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_json('json_file1.json', lines = True)

df.to_csv('ts_tweets.csv')

df = pd.read_csv('ts_tweets.csv')

df1 = df['text']

df2, emojis = [], []

# find emoji in a string
def extract_emojis(str):

	emj = ''.join(c for c in str if c in emoji.UNICODE_EMOJI)

	return emj

# find special characters in a string
pattern1 = re.compile(" S % & ' ( ) * + , - . / : ; < = >  @ [ / ] ^ _ { | } ~")

# find other usersnames tagged by the current user
pattern2 = re.compile("@[A-Za-z0-9_:]+") 

# find hashtag
pattern3 = re.compile("#[A-Za-z0-9_:]+")

# find web link
pattern4 = re.compile("https?://[A-Za-z0-9./]+")

# find the word 'RT'
pattern5 = re.compile("RT ")

# remove all the above words/characters from a tweet text
for item in df1:

    tweet = re.sub(pattern1, "", item)   
    tweet = re.sub(pattern2, "", tweet)
    tweet = re.sub(pattern3, "", tweet)
    tweet = re.sub(pattern4, "", tweet)
    tweet = re.sub(pattern5, "", tweet)
    emj = extract_emojis(list(tweet))
    tweet = re.sub('[^A-Za-z0-9 ]+', '', tweet)

    # append a cleaned-up text to a new list
    df2.append(tweet)

    # append an emoji to a list
    if emj != '': emojis += list(emj)

df3 = pd.DataFrame({'text_after': df2})

# save the text to a new csv file after cleaning up
df3.to_csv('text.csv', index = False)

# print(df3.shape)

# count the frequency of each emoji
emoji_sum = Counter(emojis)

# find the top 20 emojis that appear in tweets related to Taylor Swift
emoji_sum = emoji_sum.most_common(20)

emoji_lst, count_lst = '', []

# could not load emoji font in matplotlib, print them out instead
for (emoji, count) in emoji_sum:

    print(emoji)

    emoji_lst += emoji

    count_lst.append(count)

# find out the total number of words
text = " ".join(tweet for tweet in df3.text_after)

print("There are {} words in the combination of all tweets.".format(len(text)))

# find the 20 most common words in TS-related tweets 
def plot_20_most_common_words(data, vectorizer):

    words = count_vectorizer.get_feature_names()

    count_lst = np.zeros(len(words))

    for t in count_data:

        count_lst += t.toarray()[0]
    
    count_dict = zip(words, count_lst)

    count_dict = sorted(count_dict, key = lambda x: x[1], reverse = True)[0:20]

    words, counts = [w[0] for w in count_dict], [w[1] for w in count_dict]

    plt.figure(figsize = (10, 10))

    plt.bar(np.arange(len(words)), counts)

    plt.xticks(np.arange(len(words)), words, rotation = 90) 

    plt.xlabel('words')

    plt.ylabel('counts')

    plt.title('20 most common words')

    plt.savefig("top_20_words.png")
    
vectorizer = CountVectorizer(stop_words = 'english')

data = count_vectorizer.fit_transform(df3['text_after'])

# Visualise the 20 most common words
plot_20_most_common_words(data, vectorizer)

# Use sentiment analysis by Vader to find out the percentages of positive, neutral, positive tweets
sentiment = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(text):
    
    score = sentiment.polarity_scores(text)

    lb = score['compound']
    
    if lb >= 0.05: return 1

    elif (lb > -0.05) and (lb < 0.05): return 0

    else: return -1
    
df3['VSA'] = np.array([ sentiment_analyzer_scores(tweet) for tweet in df3['text_after'] ])

pos_tweets = [tweet for index, tweet in enumerate(df3['text_after']) if df3['VSA'][index] > 0]

neu_tweets = [tweet for index, tweet in enumerate(df3['text_after']) if df3['VSA'][index] == 0]

neg_tweets = [tweet for index, tweet in enumerate(df3['text_after']) if df3['VSA'][index] < 0]

print("Percentage of positive tweets: {}%".format(len(pos_tweets) * 100 / len(df3['text_after'])))

print("Percentage of neutral tweets: {}%".format(len(neu_tweets) * 100 / len(df3['text_after'])))

print("Percentage of negative tweets: {}%".format(len(neg_tweets) * 100 / len(df3['text_after'])))

labels = ['positive', 'neutral', 'negative']

pos = round(len(pos_tweets) * 100 / len(df3['text_after']), 1)

neu = round(len(neu_tweets) * 100 / len(df3['text_after']), 1)

neg = round(len(neg_tweets) * 100 / len(df3['text_after']), 1)

sizes = [pos, neu, neg]

explode = (0, 0, 0.1)

fig1, ax1 = plt.subplots()

ax1.pie(sizes, explode = explode, labels = labels, autopct = '%1.1f%%', shadow = True, startangle = 90)

ax1.axis('equal')  

plt.savefig("pie_chart.png")

# functions 'plot_20_most_common_word' and 'sentiment_analyzer_scores' 
# credit to 'https://towardsdatascience.com/fun-with-analyzing-billgates- tweets-twitter-apis-step-by-step-analysis-11d9c0448110'

