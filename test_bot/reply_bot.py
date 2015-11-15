import praw
import pdb
import re
import os
from credentials import *

if not  os.path.isfile("credentials.py"):
    print "You must create a config file with your username and password."
    exit(1)

user_agent = ("PyFor Eng bot 0.1")
r = praw.Reddit(user_agent=user_agent)

r.login(USERNAME, PASSWORD)

subreddit = r.get_subreddit('sandboxbox')
for submission in subreddit.get_hot(limit=5):
    submission.add_comment(submission.title)
