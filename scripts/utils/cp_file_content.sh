#!/bin/sh

: '
This script tracks the content of one file,
    and replicates in another.
'

# Default parameters, you can set both at execution
# time with $1 and $2 command line parameters
ORIGIN_FILE="$1"
DEST_FILE="$2"

# $3: If 1, dest file will be remplaced with content in
# origin file. As default, the file will not be replaced.
REPLACE=$3

if [[ $REPLACE = "" ]]; then
    REPLACE=0
fi

i=0
while IFS= read line; do
    if [[ $REPLACE -eq 1 ]]; then
        if [[ $i -eq 0 ]]; then
            echo $line > $DEST_FILE
        else
            echo $line >> $DEST_FILE
        fi
    else
        echo $line >> $DEST_FILE
    fi
    i=$(($i+1))
done < "$ORIGIN_FILE"
