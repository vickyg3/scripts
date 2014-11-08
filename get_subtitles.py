#! /usr/bin/python

import hashlib
import os
import requests
import sys

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def main():
	if len(sys.argv) != 2:
		print "Usage: %s <path_to_movie_file>" % sys.argv[0]
		sys.exit(0)
	headers = {'User-Agent' : "SubDB/1.0 (SubtitleScript/1.0; http://github.com/vickyg3/scripts)"}
	filename = sys.argv[1].strip()
	filehash = get_hash(filename)
	# search
        search_url = "http://api.thesubdb.com/?action=search&hash=%(filehash)s"
	data = requests.get(search_url % locals(), headers = headers).text
	if "en" not in data.split(","):
		print "nothing found :("
		sys.exit(0)
	# download
	srt_filename = "%s.srt" % os.path.splitext(filename)[0]
	download_url = "http://api.thesubdb.com/?action=download&hash=%(filehash)s&language=en"
	data = requests.get(download_url % locals(), headers = headers).text
	f = open(srt_filename, 'w')
	f.write(data.encode('utf-8'))
	f.close()
	print "done :)"

if __name__ == "__main__":
	main()
