#!/bin/bash

python count.py $1
#diff --side-by-side --suppress-common-lines old out | less
newfilename=$(date +%Y%m%d)
cp out old
mv out $newfilename
echo "Saved as $newfilename"
