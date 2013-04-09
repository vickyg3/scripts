# This is a monkeyrunner script
# Scramble bot used to play "Scramble with Friends!"
# Values are hard coded for nexus 7 portrait mode

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time
import trie

words = [word.strip() for word in open('dictionary.txt', 'r')]
print 'constructing data structure'
word_trie = trie.Trie()
for word in words:
    word_trie[word] = 1
print 'done'

print 'waiting for device'
device = MonkeyRunner.waitForConnection()
print 'device attached'

row_coordinates = (
                    (28, 292, 748, 184),
                    (28, 478, 748, 184)
                    (28, 668, 748, 184),
                    (28, 852, 748, 184)
                  )

input_string = raw_input("input: ").strip()
#input_string = "antdeealesesscba"
letters = [list(input_string[i:i+4]) for i in range(0,16,4)]

start_time = time.time()

n = 4
q = []
cnt = 0
small_words = []
freezes = [0, 0, 0]

found_words = trie.Trie()

def getx(y):
	return 200 * y + 100;

def gety(x):
	return 200 * x + 300

def emulate(word):
    global start_time, freezes
    for letter in word:
        device.touch(getx(letter[2]), gety(letter[1]), MonkeyDevice.DOWN_AND_UP)
        time.sleep(0.1)
    device.touch(getx(word[-1][2]), gety(word[-1][1]), MonkeyDevice.DOWN_AND_UP)
    time.sleep(0.1)
    diff = int(time.time() - start_time)
    if (diff % 40) in (0, 1, 2, 3):
        idx = 0
        if(diff > 20):
            idx = 1
        if(diff > 100):
            idx = 2
        if(not freezes[idx]):
            freezes[idx] = 1
            device.touch(200 + (200 * idx), 1200, MonkeyDevice.DOWN_AND_UP)
            time.sleep(0.1)

def tuple_to_string(word):
    return ''.join([actual_word for actual_word, d1, d2 in word])

def process(word):
    global cnt, q, device, start_time, small_words
    string = tuple_to_string(word)
    # string should be a valid word of length atleast 4 and hasn't been seen already
    add_word = True
    try:
        dummy = word_trie[string] # if this fails, then word not found 
    except trie.NeedMore:
        add_word = True
    except:
        add_word = False
    else:
        try:
            dummy = found_words[string]
        except:
            found_words[string] = 1
            if(len(string) > 4):
                print cnt, ":", string
                print time.time() - start_time
                emulate(word)
                cnt += 1
            elif len(string) > 1:
                small_words.append(word[:])
    if add_word:
        q.append(word)

# start with single letter elements
for i in range(n):
    for j in range(n):
        process([(letters[i][j], i, j)])

while len(q) > 0:
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

# output all the small words
for small_word in reversed(small_words):
    emulate(small_word)
    print cnt, ":", tuple_to_string(small_word)
    print time.time() - start_time
    cnt += 1