import praw, json, os, re, grequests
from defusedxml import ElementTree 
from time import sleep

user_agent = ("hpp3_test_0.1")


r = praw.Reddit(user_agent = user_agent)
subreddit = r.get_subreddit("sandboxbox")

with open('credentials.json', 'r') as f:
    credentials = json.load(f)


r.login(credentials["username"], credentials["password"], disable_warning=True)

if not os.path.isfile('processed'):
    processed = {}
else:
    with open('processed', 'r') as f:
        processed = json.load(f)
    
comment = None

def reddit_format(text):
    return re.sub("^(?=\w)",'>', text, flags=re.MULTILINE);

def format(response):
    text = response.text
    et = ElementTree.fromstring(text)
    return reddit_format(et.find('post').find('content').text)

while True:
    try:
        for submission in subreddit.get_new(limit = 20):
            matches = re.findall("http://www.twitlonger.com/show/(\w+)", submission.url, re.IGNORECASE)
            matches += re.findall("http://www.twitlonger.com/show/(\w+)", submission.selftext, re.IGNORECASE)
            if matches:
                urls = ["http://www.twitlonger.com/api_read/%s" % match for match in matches]
                rs = (grequests.get(u) for u in urls)
                responses = grequests.map(rs)
                txt = '%d Twitlonger %s found.\n\n' % (len(responses), 'post' if len(responses) == 1 else 'posts') + '\n***\n'.join(map(format, responses)) + '\n***\nThis comment was created by a bot.  \n[Source Code](https://github.com/jsshao/reddit_bots)'
                if submission.id not in processed:
                    comment = submission.add_comment(txt)
                    processed[submission.id] = comment.permalink
                else:
                    comment = r.get_submission(processed[submission.id]).comments[0]
                    comment.edit(txt)
    finally:
        with open('processed', 'w') as f:
            json.dump(processed, f)
    sleep(60)
