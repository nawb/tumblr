#!/bin/bash

python count.py
if [[ $1 == "cat" ]]; then
    cat out
fi
