# This is a monkeyrunner script
# Scramble bot used to play "Scramble with Friends!"
# Values are hard coded for nexus 7 portrait mode

#from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time

words = set([word.strip() for word in open('words.txt', 'r')])
#print 'waiting for device'
#device = MonkeyRunner.waitForConnection()
#print 'device attached'


#input_string = raw_input("input: ").strip()
input_string = "csteonegdrunodmb"
letters = [list(input_string[i:i+4]) for i in range(0,16,4)]

start_time = time.time()

n = 4
q = []
cnt = 0

limit = 300
found_words = {}

def getx(y):
	return 200 * y + 100;

def gety(x):
	return 200 * x + 300

def process(word):
    global cnt, q, device, found_words, start_time
    string = ''.join([actual_word for actual_word, d1, d2 in word])
    # string should be a valid word of length atleast 2 and hasn't been seen already
    if string in words and len(string) > 1 and not found_words.has_key(string):
        print cnt, ":", string
        found_words[string] = 1
        print time.time() - start_time
        # emulate the touch
        #for letter in word:
        #	device.touch(getx(letter[2]), gety(letter[1]), MonkeyDevice.DOWN_AND_UP)
		#time.sleep(0.1)
        #device.touch(getx(word[-1][2]), gety(word[-1][1]), MonkeyDevice.DOWN_AND_UP)
	    #time.sleep(0.1)
        cnt += 1
    q.append(word)

# start with single letter elements
for i in range(n):
    for j in range(n):
        process([(letters[i][j], i, j)])

while cnt < limit:
    head = q[0]
    del q[0]
    # append one letter in each direction
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            row = head[-1][1] + i
            col = head[-1][2] + j
            # bounds check
            if row < 0 or col < 0 or row > n - 1 or col > n - 1:
                continue
            # check for repetition
            repeated = False
            for dummy, old_row, old_col in head:
                if old_row == row and old_col == col:
                    repeated = True
                    break
            if repeated:
                continue
            old_head = head[:]
            head.append((letters[row][col], row, col))
            process(head)
            head = old_head
