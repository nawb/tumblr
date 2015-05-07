#!/bin/bash

python count.py $1
diff --side-by-side --suppress-common-lines old out | less
