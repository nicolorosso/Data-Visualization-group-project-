#scraper parallelized
import concurrent.futures
import tweets_scraper #scraper save in a .py file to parallelized the operation

def scraper(parole, since, until):
    tweets_list1 = []
    with concurrent.futures.ProcessPoolExecutor(30) as executor:
        results = [executor.submit(tweets_scraper.scrape_tweets_for_user, p,since, until) for p in parole]
        for future in concurrent.futures.as_completed(results):
            tweets_list1.extend(future.result())

    df = pd.DataFrame(tweets_list1, columns=['url',
                                              'datetime', 
                                              'tweet_Id',
                                             'conversation_ID',
                                              'text', 
                                              'username', 
                                             'displayname',
                                             'reply_count',
                                             'retweet_count',
                                             'quote_count',
                                             'retweeted_tweet',
                                             'quoted_tweet',
                                             'mentioned_users'
                                              ])
    return df
  
parole = ['elections', 'fraud', 'democrats', 'riggedelection', 'SharpieGate', 'democrats', 'capitol hill', 'biden', 'trump', 'georgia']
start_date = "2020-10-30"
end_date = "2021-01-06"
tweets_df2 = scraper(parole, start_date, end_date)

#avoid snscrape classes before saving
df = tweets_df2.copy().explode('mentioned_users')

#fill the Nan values
df = df.fillna(value=np.nan)

#convertire mentioned_users and quoted_users in strings
df['strquoted']= df['quoted_tweet'].astype(str)
df['strmentioned']= df['mentioned_users'].astype(str)

#save the cleaned file in order to perform the analysis
df.to_csv('ADD_PATH', index=False)
