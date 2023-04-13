# Ego Network Structure on Twitter: a graph-based approach to detect viral diffusion of information amongst community

## Group D: Federico Jacopo Baldoni, Giovanni Raimondo Quaratino, Nicolò Rosso

Abstract: 

Online Social Media (OSMs) are increasingly becoming a major source of information. According  to the Reuters Institute Digital News Report 2022, social media has become the preferred source of information for 28% of the users across different markets. 
The importance of social media as the main source of information for users raises many questions about how information is disseminated. In this context, a concept borrowed from sociology comes in handy: ego networks. An ego network is defined as a portion of a social network formed of a given individual, termed ego, and the other persons with whom he/she has a social relationship, termed alters. In the context of social media, these alters take the form of followers. The objective of this study is to highlight the role of ego-networks in the dissemination of information on Twitter, through a graph-based approach.

Our Approach: 

1. Data Mining
2. Network Modelling
3. Community Detection
4. Observations & Analysis

Task 3.1: Select a Dataset 

To analyze the user community on Twitter, this research will make use of Snscrape, an unofficial Twitter API that allows high numbers by cross-referencing keyword searches and time windows. The use of this api will be completed on Python, and it will be made available for users through its implementation on Streamlit, a Python library that allows for the creation of interactive dashboards. The goal of the research is to take a graph-based approach to highlight the role of ego-networks in information dissemination. To carry out this proposition, the API will allow the following information to be obtained: 

date: The date of the tweet; 
rawContent: the content of the tweet; 
id: The ID of the tweet, that states its unicity; 
user: The users who tweeted; 
replyCount: The count of the users who replied to the tweet; 
retweetCount: The count of users who retweeted to the tweet; 
likeCount: The number of likes for the tweet; 
quoteCount: The number of users who quoted the tweet; 
conversationId: When Tweets are posted in response to a Tweet (known as a reply), or in response to a reply, there is now a defined conversation_id on each reply, which matches the Tweet ID of the original Tweet that started the conversation. 


Task 3.2: Perform a task analysis

The use of a graph-based approach will make it possible to visualize the role of communities in the dissemination of information. The roberta-large-mnli model will be implemented to find such communities based on the level of agreement among different Tweets. In addition, to identify the role of ego networks, author quality will be considered: This measure aims to consider the importance of the echo in the world of social media, therefore highlighting those words being written by very "followed" and "retweeted" authors. 

Task 3.3: Design the visualization

This image highlights our methodology. It is important to underline how in a twitter social network there are three type of interactions among users:
Quotes of a tweet;
Reply to a tweet; 
Mention of a user. 


In order to highlight the presence of a community structure within the ego-network of twitter 
users, the proposed research wants to come up with different network graphs. 

In this first representation, thanks to Pyvis, we analyzed the ego-network structure of Twitter based on the interactions among users. Every node is a user who interacts with another user. Our assumption is: The higher number of interactions towards a specific user will allow us to detect such ego-network. 

Moreover, to detect the degree of polarization among communities, we computed the level of agreements between texts.

The next steps of the proposed research will be as follows. At first, to better delineate the level of polarization and how some users may contribute to the spread of such phenomena. Second, to highlight the role of ego-network in the so-called information dissemination structure.
