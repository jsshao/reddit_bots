import praw
import pdb
import re
import os
from PIL import Image
import cStringIO
from StringIO import StringIO
import urllib
import sys

if not os.path.isfile("config.py"):
    print "You must create a config file with your username and password."
    exit(1)

user_agent = ("JoJoChuu Bot 0.1")

r = praw.Reddit(user_agent = user_agent)
r.login(REDDIT_USERNAME, REDDIT_PASS)

subreddit = r.get_subreddit("sandboxbox")

def load_and_resize_image(img, antialias, maxLen):

    # force image to RGBA - deals with palettized images (e.g. gif) etc.
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # resize up or down so that longer side of image is maxLen
    if maxLen is not None:
        native_width, native_height = img.size
        rate = float(maxLen) / max(native_width, native_height)
        width = int(rate * native_width)
        height = int(rate * native_height)

        if native_width != width or native_height != height:
            img = img.resize((width, height), Image.ANTIALIAS
                             if antialias else Image.NEAREST)

    return img

def alpha_blend(src, dst):
    # Does not assume that dst is fully opaque
    # See https://en.wikipedia.org/wiki/Alpha_compositing - section on "Alpha
    # Blending"
    print "alpha_blend"
    src_multiplier = (src[3] / 255.0)
    dst_multiplier = (dst[3] / 255.0) * (1 - src_multiplier)
    result_alpha = src_multiplier + dst_multiplier
    if result_alpha == 0:       # special case to prevent div by zero below
        return (0, 0, 0, 0)
    else:
        return (
            int(((src[0] * src_multiplier) +
                (dst[0] * dst_multiplier)) / result_alpha),
            int(((src[1] * src_multiplier) +
                (dst[1] * dst_multiplier)) / result_alpha),
            int(((src[2] * src_multiplier) +
                (dst[2] * dst_multiplier)) / result_alpha),
            int(result_alpha * 255)
        )


def generate_grayscale_for_image(pixels, width, height, bgcolor):
    # grayscale
    print "generate_grayscale_for_image"
    color = "MNHQ$OC?7>!:-;. "

    string = ""
    # first go through the height,  otherwise will rotate
    for h in xrange(height):
    	string += "    "
        for w in xrange(width):

            rgba = pixels[w, h]

            # If partial transparency and we have a bgcolor, combine with bg
            # color
            if rgba[3] != 255 and bgcolor is not None:
                rgba = alpha_blend(rgba, bgcolor)

            # Throw away any alpha (either because bgcolor was partially
            # transparent or had no bg color)
            # Could make a case to choose character to draw based on alpha but
            # not going to do that now...
            rgb = rgba[:3]

            string += color[int(sum(rgb) / 3.0 / 256.0 * 16)]

        string += "\n"

    return string

for submission in subreddit.get_new():
	for comment in submission.comments:
		body = comment.body
		link = re.search("(?P<url>https?://[^\s]+)", body)
		if link is not None and (link.endswith(".png") or link.endswith(".jpg"):
			link = link.group("url")

			file = cStringIO.StringIO(urllib.urlopen(link).read())
			img = Image.open(file)
			width, height = img.size
			img = img.resize((width, int(height * 0.5)), Image.ANTIALIAS)
			img = load_and_resize_image(img, True, 75)
			pixel = img.load()

			width, height = img.size

			string = generate_grayscale_for_image(pixel, width, height, None)

	        sys.stdout.write(string)

			sys.stdout.flush()
			comment.reply(string)