import praw
import pdb
import re
import os
import Image
import urllib
import cStringIO
from PIL import Image
from pytesseract import image_to_string
from credentials import *

def transcribe(submission, img):
    x, y = img.size
    scale = min(8000/x, 8000/y)
    im_resized = img.resize((x * scale, y*scale), Image.ANTIALIAS)
    text = image_to_string(im_resized).split('\n')
    text = [">" + i + " " for i in text]
    text = '\n'.join(text)
    text = "This transcription was performed by OCR bot\n" + text
    text += "\n\n ***\n\nThis message was created by a bot\n\n"
    text += "[\[Source Code\]](https://github.com/jsshao/reddit_bots)"
    
    submission.add_comment(text)

if not  os.path.isfile("credentials.py"):
    print "You must create a config file with your username and password."
    exit(1)

user_agent = ("PyFor Eng bot 0.1")
r = praw.Reddit(user_agent=user_agent)

r.login(USERNAME, PASSWORD, disable_warning=True)

subreddit = r.get_subreddit('sandboxbox')

if not os.path.isfile("history.txt"):
    history = []
else:
    with open("history.txt", "r") as f:
       history = f.read()
       history = history.split("\n")
       history = filter(None, history)

for submission in subreddit.get_hot():
    if submission.id in history:
        continue

    if submission.url.endswith(".png") or submission.url.endswith(".jpg"):
        file = cStringIO.StringIO(urllib.urlopen(submission.url).read())
        img = Image.open(file)
        transcribe(submission, img)
    elif "gyazo.com" in submission.url:
        file = cStringIO.StringIO(urllib.urlopen(submission.url + ".png").read())
        img = Image.open(file)
        transcribe(submission, img)

    history.append(submission.id)

with open("history.txt", "w") as f:
    for post_id in history:
        f.write(post_id + "\n")
