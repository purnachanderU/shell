#!/bin/bash
echo "Enter the number"
read marks

if [ $marks -lt 33]; then
    echo "Fail"
elif [ $marks -lt 50 ]; then
    echo "Second class"
elif [ $marks -lt 60 ]; then
    echo "First class"
else
    echo "Distinction"
fi