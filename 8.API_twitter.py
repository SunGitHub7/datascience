import pickle
import os
import twitter
import pandas as pd
from collections import Counter
import json

# Get Acess to the twitter and Make Object.
p1 = 'secret_twitter_credentials.pkl'
# os.remove(p1)  # use this command if you have regenerate Twitter attributes as mentioned below
if not os.path.exists(p1):  # if given file does not exist do this data entry
    Twitter = {}
    Twitter['Consumer Key'] = '--------------------------------'
    Twitter['Consumer Secret'] = '----------------------------------------------------'
    Twitter['Access Token'] = '------------------------------------------'
    Twitter['Access Token Secret'] = '--------------------------------------'
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
IND_woeid = 23424848
wrld_woeid = 1
us_woeid = 23424977
sndg_us_woeid = 2487889

wrld_trnds = twitter_api.trends.place(_id=wrld_woeid)  # By default trends.place give 50 trends
us_trnds = twitter_api.trends.place(_id=us_woeid)
# IND_trnds = twitter_api.tremds.place(_id=IND_woeid)
sndg_us_trnds = twitter_api.trends.place(_id=sndg_us_woeid)

# Displaying API trends in well structured JSON format------------------------------------------------------------------
# print(json.dumps(us_trnds[0]['trends'], indent=1))

# COMPUTING THE INTERSECTION OF TWO SETS OF TRENDS Generating Dictionary with key as Location

trnd_set = {}
trnd_set['World'] = list(set([trend['name'] for trend in wrld_trnds[0]['trends']]))
trnd_set['US'] = list(set([trend['name'] for trend in us_trnds[0]['trends']]))
trnd_set['San_Diego'] = list(set([trend['name'] for trend in sndg_us_trnds[0]['trends']]))
wrld_us_set = list(set(trnd_set['San_Diego']).intersection(trnd_set['US']).intersection(trnd_set['World']))  # common trends in US and San Diego
print(wrld_us_set)
#  Convert all trends into pandas Data Frame---------------------------------------------------------------------------
df_trend = pd.DataFrame({key: pd.Series(value) for key, value in trnd_set.items()})  # for differnt length of trends

# Twitter Search--------------------------------------------------------------------------------------------------------
topic = wrld_us_set[0]
num = 100

srch_rslt = twitter_api.search.tweets(q=topic, count=num)
statuses = srch_rslt['statuses']  # Here there are duplicate record is also possible
# print(json.dumps(statuses, indent=1))  # JSON format to see statuses in roper structured manner
nit_text = []
nit_stts = []

for s in statuses:
    if s['text'] not in nit_text:
        nit_text.append(s['text'])
        nit_stts.append(s)

# print(json.dumps(nit_stts[1]['text'], indent=1))

screen_name = [user_mention['screen_name']
               for s in nit_stts
               for user_mention in s['entities']['user_mentions']]
hashtag = [hashtag['text']
           for s in nit_stts
           for hashtag in s['entities']['hashtags']]

#  Collection of All the WORD from tweet
word = [w for t in nit_text for w in t.split()]

# Explore the items for each of this in Data Frame format-----------------------------------------------------------
dctnry = {'TEXT': pd.Series(nit_text), 'SCREEN_NAME': pd.Series(screen_name),
        '#-TAG': pd.Series(hashtag), 'WORD': pd.Series(word)}
df_search = pd.DataFrame(dctnry, columns=['TEXT','SCREEN_NAME','#-TAG','WORD'])
print(df_search)

# Frequency of This Collections with proper display --------------------------------------------------------------------
itm = ['TEXT', 'Screen Name', 'Hash(#)-Tage']
for idx, item in enumerate([nit_text, screen_name, hashtag]):
    c = Counter(item)
    cnt_itm = c.most_common()
    df_cnt_itm = pd.DataFrame(cnt_itm, columns=[itm[idx], 'Frequency'])
    print(df_cnt_itm,'\n')

