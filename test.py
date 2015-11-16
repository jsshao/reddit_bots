import praw, json, os, re, grequests
from defusedxml import ElementTree 

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

def format(response):
    text = response.text
    et = ElementTree.fromstring(text)
    return reddit_format(et.find('post').find('content').text)

try:
    for submission in subreddit.get_hot(limit = 10):
        matches = re.findall("http://www.twitlonger.com/show/(\w+)", submission.url, re.IGNORECASE)
        matches += re.findall("http://www.twitlonger.com/show/(\w+)", submission.selftext, re.IGNORECASE)
        if matches:
            urls = ["http://www.twitlonger.com/api_read/%s" % match for match in matches]
            rs = (grequests.get(u) for u in urls)
            responses = grequests.map(rs)
            print map(format, responses)
            # if submission.id not in processed:
            #     comment = submission.add_comment("imgur test")
            #     processed[submission.id] = comment.permalink
            # else:
            #     print "already processed %s" % submission.id
            #     comment = r.get_submission(processed[submission.id]).comments[0]
            #     comment.edit(str(comment) + " edited")
finally:
    with open('processed', 'w') as f:
        json.dump(processed, f)