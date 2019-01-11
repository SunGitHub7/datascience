# get modules required to work with twitter APP
import pickle
import os
import twitter
import pandas as pd
from collections import Counter
import json
import matplotlib.pyplot as mp


# Get Acess to the twitter and Make Object.
p1 = 'secret_twitter_credentials.pkl'
# os.remove(p1)  # use this command if you have regenerate Twitter attributes as mentioned below
if not os.path.exists(p1):  # if given file does not exist do this data entry
    Twitter = {}
    Twitter['Consumer Key'] = '-----------------------------------------------'
    Twitter['Consumer Secret'] = '--------------------------------'
    Twitter['Access Token'] = '-----------------------------------------'
    Twitter['Access Token Secret'] = '--------------------------------------u'
    with open(p1,'wb') as f:  # Here we are writting Twitter object into .pkl file
        pickle.dump(Twitter,f)

else:
    Twitter = pickle.load(open(p1,'rb'))  # if .pkl file exist then just read it into Twitter object


# Authentication Step for acceseing Data-------------------------------------------------------------------------------
auth = twitter.oauth.OAuth(Twitter['Access Token'],
                           Twitter['Access Token Secret'],
                           Twitter['Consumer Key'],
                           Twitter['Consumer Secret'],
                           )
twitter_api = twitter.Twitter(auth=auth)

# Retrieving Trends w.r.t. woeid(Where On Earth Identifiers)-----------------------------------------------------------
IND = 23424848
WRLD = 1

wrld_trnds = twitter_api.trends.place(_id=WRLD)  # By default trends.place give 50 trends
IND_trnds = twitter_api.trends.place(_id=IND)

# Displaying API trends in well structured JSON format------------------------------------------------------------------
# print(json.dumps(IND_trnds[0]['trends'], indent=1))

# COMPUTING THE INTERSECTION OF TWO SETS OF TRENDS Generating Dictionary with key as Location

trnd_set = {}
trnd_set['World'] = list(set([trend['name'] for trend in wrld_trnds[0]['trends']]))
trnd_set['INDIA'] = list(set([trend['name'] for trend in IND_trnds[0]['trends']]))
IND_trnd = trnd_set['INDIA']
wrld_ind_set = list(set(trnd_set['INDIA']).intersection(trnd_set['World']))  # common trends in India and world
# print(IND_trnd)
#  Convert all trends into pandas Data Frame---------------------------------------------------------------------------
df_trend = pd.DataFrame({key: pd.Series(value) for key, value in trnd_set.items()})  # for differnt length of trends
# print(df_trend)
# df_trend.to_csv('trend.csv')  # Here we will get recent trends in Twitter India and World

# Twitter Search with hash-tags related to #2019Election  -----------------------------------------------------------
topic = '#2019Elections'
num = 100
srch_rslt = twitter_api.search.tweets(q=topic, count=num)
# print(srch_rslt)
statuses = srch_rslt['statuses']  # Here there are duplicate record is also possible
# print(json.dumps(statuses, indent=1))  # JSON format to see statuses in roper structured manner
nit_text = []
nit_stts = []
#
for s in statuses:
    if s['text'] not in nit_text:
        nit_text.append(s['text'])
        nit_stts.append(s)
#
# print(json.dumps(nit_stts[1]['text'], indent=1))

screen_name = [user_mention['screen_name']
               for s in nit_stts
               for user_mention in s['entities']['user_mentions']]
hashtag = [hashtag['text']
           for s in nit_stts
           for hashtag in s['entities']['hashtags']]

#  Collection of All the WORD from tweet
word = [w for t in nit_text for w in t.split()]
print(word)
#
# Explore the items for each of this in Data Frame format-----------------------------------------------------------
dctnry = {'TEXT': pd.Series(nit_text), 'SCREEN_NAME': pd.Series(screen_name),
        '#-TAG': pd.Series(hashtag), 'WORD': pd.Series(word)}
df_search = pd.DataFrame(dctnry, columns=['TEXT','SCREEN_NAME','#-TAG','WORD'])
Elctin19_df = df_search[df_search['#-TAG'] == '2019Elections']
Elctin19_df=Elctin19_df.dropna()

Elctin19_df[['TEXT','#-TAG','SCREEN_NAME']].to_csv('electionTweets.csv')  # Here we will get tweets, screen name, # Tag,

# Frequency of This Collections with proper display --------------------------------------------------------------------
cnt = Counter(Elctin19_df['SCREEN_NAME'])
most_cnt = cnt.most_common(10)
print(most_cnt)
df_most_cnt = pd.DataFrame(most_cnt, columns=['SCREEN NAME', 'Frequency'])
mp.barh(df_most_cnt[df_most_cnt.columns[0]], df_most_cnt[df_most_cnt.columns[1]])
mp.tight_layout()
mp.title('Most Common SCREEN NAME for 2019 Elections')
mp.ylabel('SCREEN NAME')
mp.xlabel('Number of Occurrence')
mp.show()
