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
    return text

def parse_url(url, img_list):
    if url.endswith(".png") or url.endswith(".jpg"):
        file = cStringIO.StringIO(urllib.urlopen(url).read())
        img = Image.open(file)
        img_list.append(img)  
    elif "gyazo.com" in url:
        file = cStringIO.StringIO(urllib.urlopen(url + ".png").read())
        img = Image.open(file)
        img_list.append(img)  

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

for submission in subreddit.get_new():
    if submission.id in history:
        continue

    img_list = []
    parse_url(submission.url, img_list)
    matches = re.findall("((http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)", submission.selftext, re.IGNORECASE)

    matches = [i[0] for i in matches]
    for url in matches:
        parse_url(url, img_list)

    text = "There were " + str(len(img_list)) + " image[s] found in this post.\n\n"
    text += "This transcription was performed by OCR bot\n\n\n\n"
    for img in img_list:
        text += transcribe(submission, img)
        text += "\n\n ***\n\n"

    text += "This message was created by a bot\n\n"
    text += "[\[Source Code\]](https://github.com/jsshao/reddit_bots)"

    if len(img_list) != 0:
        submission.add_comment(text)

    history.append(submission.id)

with open("history.txt", "w") as f:
    for post_id in history:
        f.write(post_id + "\n")
