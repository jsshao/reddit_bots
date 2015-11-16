import os
import subprocess
import commands
import glob

def getcaption(url): 
	subprocess.call(["youtube-dl", "--all-subs", "--skip-download", "-otest", url])

	if not os.path.isfile("posts_replied_to.txt"):
		captions = []
	else:
		with open("test.en.srt", "r") as f:
			captions = f.read()
			captions = captions.split("\n")

	i = 0
	captionsOut = []
	while i < len(captions):
		if i > len(captions) - 3:
			break
		index = captions[i]
		time = captions[i+1]
		i+=2
		text = ""
		while captions[i] != "":
			text += captions[i] + " "
			i+=1
		i+=1
		captionsOut.append({'time':time, 'text':text})
		
	for fl in glob.glob("*.srt"):
		os.remove(fl)
	return captionsOut
		
#~ print captionsOut
