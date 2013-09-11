#! /usr/bin/python

# Code is licensed under WTFPL
# http://www.wtfpl.net/

import json
import os
import re
import sys
import urllib2

def die():
	print >>sys.stderr, "Sorry, It won't work! :("
	sys.exit(1)

def main():
	
	### YOU CAN MODIFY THESE VARIABLES AS PER YOUR ENVIRONMENT ###
	# path to the ffmpeg command
	ffmpeg_cmd = "ffmpeg"
	# amount of seconds to go back from the end of the song
	end_delta = 5
	# host where VLC is listening on
	host = "127.0.0.1"
	# port number where VLC is listening on
	port = "8080"
	### END OF CONFIGURABLE VARIABLES
	### Do not change anything after this unless you know what you are doing

	silence_exp = re.compile(r'.* silence_end: ([^ ]+).*')
	url = "http://%(host)s:%(port)s" % locals()
	playlist_url = "%(url)s/requests/playlist.json" % locals()
	status_url = "%(url)s/requests/status.json" % locals()
	resume_url = "%(url)s/requests/status.xml?command=pl_forceresume" % locals()
	seek_url = url + "/requests/status.xml?command=seek&val=%s"

	# get the file that's currently playing
	current_file = None
	try:
		files = json.load(urllib2.urlopen(playlist_url))['children'][0]['children']
		for f in files:
			if f.get('current', None):
				current_file = f.get('uri', None)
				break
	except:
		# TODO: may be try xml ?
		die()

	# get the position currently being played
	try:
		status = json.load(urllib2.urlopen(status_url))
	except:
		# TODO: may be try xml ?
		die()

	if not current_file or not status:
		die()

	try:
		# detect the next silence
		current_time = status['time']
		ffmpeg = """
					%(ffmpeg_cmd)s -ss %(current_time)s -i "%(current_file)s" \
					-t 600 -vn -af silencedetect=noise=0.1 -f null - 2>&1 | 
					grep -m 1  'silence_end'""" % locals()
		seek_position = silence_exp.match(os.popen(ffmpeg).read().strip()).groups()[0]
		seek_position = int(current_time) + int(float(seek_position)) - end_delta

		# seek to the new position
		dummy = urllib2.urlopen(seek_url % str(seek_position)).read()

		# start playing if the video wasn't playing already
		dummy = urllib2.urlopen(resume_url).read()
	except:
		die()

if __name__ == "__main__":
	main()