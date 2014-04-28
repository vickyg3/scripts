#! /bin/bash

wget "http://www.bing.com/search?q=$(cat query)" -O data.html 2> /dev/null
for i in {0..3}; do
	n=$(grep -oi "$(cat o${i})" data.html | wc -l)
	echo "${n} ${i}" >> numbers
done
sort -nr -k1 numbers | head -n 1 | cut -d ' ' -f2
rm numbers
