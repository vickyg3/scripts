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
        print "Usage %s <movie_file>" % sys.argv[0]
        sys.exit(0)
    search_url = "http://api.thesubdb.com/?action=search&hash=%s"
    user_agent = "SubDB/1.0 (FoamsNet/1.0; http://github.com/vickyg3/scripts)"
    headers = {
        'User-Agent': user_agent
    }
    file_hash = get_hash(sys.argv[1])
    data = requests.get(search_url % file_hash, headers = headers).text
    if 'en' not in data.split(','):
        print 'done :) no english subtitles found :('
        return
    download_url = "http://api.thesubdb.com/?action=download&hash=%s&language=en"
    data = requests.get(download_url % file_hash, headers = headers).text
    file_dir = os.path.dirname(os.path.abspath(sys.argv[1]))
    file_name = os.path.splitext(sys.argv[1])[0] + ".en.srt"
    srt_file = os.path.join(file_dir, file_name)
    f = open(srt_file, 'w')
    f.write(data.encode('utf-8'))
    f.close()
    print 'done :)'

if __name__ == "__main__":
    main()