#! /usr/bin/python

# Simple implementation of a token bucket algorithm.
# Solves this question: Write a function that returns false if it has been
# called n times or more in the last m seconds and returns true otherwise.
#
# For explanation on Token Bucket: http://en.wikipedia.org/wiki/Token_bucket

import time

n = 5
m = 20

rate = 1.0 * n # token bucket's rate (number of tokens allowed)
time_interval = 1.0 * m # token bucket's time interval ("rate" number of tokens
                        # are allowed per "time_interval" seconds.
allowed = rate - 1 # initial number of tokens allowed.
last_called = time.time()


# Key points (for myself if i read it a few years later):
#   * A token is added for every second since last call and current call at the
#     rate of rate / time_interval and capped at "rate".
#   * Return False if < 1 token is available
#   * Return True if 1 or more tokens are available and reduce the token count
#     by 1.
def rate_limited_function():
    global last_called, rate, time_interval, allowed
    current_time = time.time()
    seconds_since_last_call = current_time - last_called;
    last_called = current_time;
    allowed += seconds_since_last_call * rate / time_interval;
    if allowed > rate: # clamp allowed so that it does not exceed rate.
        allowed = rate - 1
    if allowed < 1:
        return False
    allowed -= 1
    return True

def call():
    print "Calling..", rate_limited_function(),
    print "Allowed:", allowed

def main():
    for i in range(10):
        call()
        if i < 5:
            time.sleep(1)
    time.sleep(20)
    for i in range(10):
        call()
        if i < 5:
            time.sleep(1)

# output of above sample calls:
# ./token_bucket.py
# Calling.. True Allowed: 3.00000423193
# Calling.. True Allowed: 2.25029397011
# Calling.. True Allowed: 1.50057971478
# Calling.. True Allowed: 0.750869512558
# Calling.. True Allowed: 0.00115746259689
# Calling.. False Allowed: 0.251442730427
# Calling.. False Allowed: 0.251454472542
# Calling.. False Allowed: 0.251457214355
# Calling.. False Allowed: 0.251459717751
# Calling.. False Allowed: 0.251462519169
# Calling.. True Allowed: 3.0
# Calling.. True Allowed: 2.25028550625
# Calling.. True Allowed: 1.5005697608
# Calling.. True Allowed: 0.750821471214
# Calling.. True Allowed: 0.00111275911331
# Calling.. False Allowed: 0.25140273571
# Calling.. False Allowed: 0.251414477825
# Calling.. False Allowed: 0.251417517662
# Calling.. False Allowed: 0.251420259476
# Calling.. False Allowed: 0.251422762871

if __name__ == "__main__":
    main()
