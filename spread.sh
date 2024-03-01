#!/bin/bash

DIR=${1: '-r'}
file=${@: -1}  # Get the last argument

for dir in $DIR
do
    cp "$file" "$dir"
done