#define a function to parallelize your scraping. Essential if you are running on jupyter notebook
import snscrape.modules.twitter as sntwitter
def scrape_tweets_for_user(topic,since, until):
    tweets_list1 = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{topic} since:{since} until:{until}").get_items()):
        if i>15000:
            break
        tweets_list1.append([tweet.url,
                            tweet.date, 
                            tweet.id,
                             tweet.conversationId,
                            tweet.content,
                            tweet.user.username,
                             tweet.user.displayname,
                             tweet.replyCount,
                             tweet.retweetCount, 
                             tweet.quoteCount,
                             tweet.retweetedTweet,
                             tweet.quotedTweet,
                             tweet.mentionedUsers
                             ])
    return tweets_list1
