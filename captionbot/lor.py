import praw
import pdb
import re
import os
from caption import *
from config_bot import *

user_agent = ("lor 0.1")
r = praw.Reddit(user_agent = user_agent)
r.login(USERNAME, PASSWORD)

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
       posts_replied_to = f.read()
       posts_replied_to = posts_replied_to.split("\n")
       posts_replied_to = filter(None, posts_replied_to)

subreddit = r.get_subreddit('sandboxbox')
for submission in subreddit.get_hot(limit=5):
	if submission.id not in posts_replied_to:
		if 'youtube.com' in submission.url:
			commentObj = submission
			captionsOut = getcaption(submission.url) 
			first = True;
			comment = "";
			for caption in captionsOut:
				temp = comment
				comment += caption["time"] + ":	" + caption["text"]	+ "\n\n"
				if len(comment) > 10000: 
					if (first):
						commentObj = commentObj.add_comment(temp)
						first = False
					else:
						commentObj = commentObj.reply(temp)
					comment = caption["time"] + ":	" + caption["text"]	+ "\n\n"
			posts_replied_to.append(submission.id)

with open("posts_replied_to.txt", "w") as f:
	for post_id in posts_replied_to:
		f.write(post_id + "\n")
					
