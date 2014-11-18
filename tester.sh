#!/bin/bash
clear

TestFile() {
  python2.7 src/Manager.py $1
}

for FILE in $(ls inputs)
do
  echo "CURRENTLY TESTING $FILE"
  TestFile "inputs/$FILE"
  echo "------------------------------"
done
