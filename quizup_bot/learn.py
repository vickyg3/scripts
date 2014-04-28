# this is a monkeyrunner script

import csv
import time
import sys
import re
import os

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

def shootQuestions(device):
	# scroll down to the questions
	device.drag((400, 1100), (400, 200))
	device.drag((400, 1100), (400, 200))
	device.drag((400, 1100), (400, 600))
	time.sleep(1)
	# take snapshot and store
	for i in range(7):
		img = device.takeSnapshot()
		q = img.getSubImage((141, 354, 489, 171))
		a = [0, 0, 0, 0]
		x = 189
		w = 391
		h = 110
		a[0] = img.getSubImage((x, 530, w, h))
		a[1] = img.getSubImage((x, 658, w, h))
		a[2] = img.getSubImage((x, 787, w, h))
		a[3] = img.getSubImage((x, 915, w, h))
		img.writeToFile('data/img%d.png' % i)
		q.writeToFile('data/q%d.png' % i)
		for j in range(1, 5):
			a[j - 1].writeToFile('data/a%d_%d.png' % (i, j))
		# scroll to next question
		if i != 6:
			device.drag((700, 600), (200, 600))
			time.sleep(1)

def recordScreens(device):
	pattern = re.compile('[\W_]+')
	fp = open('data/answers/general_knowledge.csv', 'rb')
	r = csv.reader(fp)
	data = {}
	for row in r:
		data[row[0]] = row[1]
	fp.close()
	cnt = 0
	while True:
		dummy = raw_input('enter ')
		if dummy.strip() == 'q':
			break
		img = device.takeSnapshot()
		img.writeToFile('data/samples/%d.png' % (cnt + 100))
		cnt += 1
		img.getSubImage((0, 110, 768, 283)).writeToFile('data/run/q.png')
		q = os.popen('tesseract data/run/q.png out 2> /dev/null; cat out.txt').read().replace('\n', ' ').strip()
		question = q
		print q
		q = pattern.sub('', q)
		q = q.lower()
		print q
		x =85
		w = 600
		h = 155
		yy = [400, 600, 800, 1000]
		for index, y in enumerate(yy):
			img.getSubImage((x,y, w, h)).writeToFile('data/run/a.png')
			a = os.popen('tesseract data/run/a.png out 2> /dev/null; cat out.txt').read().replace('\n', ' ').strip()
			f = open('o%d' % index, 'w')
			f.write(a.lower())
			print a.lower()
			f.close()
		print 'searching internet'
		f = open('query', 'w')
		f.write(question)
		f.close()
		answer_index = os.popen('./find_answer.sh').read().strip()
		print 'answer is ', answer_index
	shootQuestions(device)

print 'waiting for device'
device = MonkeyRunner.waitForConnection()
print 'device found'
print 'recording'
recordScreens(device)
print 'done :)'
sys.exit(0)
print 'shooting'
shootQuestions(device)
print 'done :)'