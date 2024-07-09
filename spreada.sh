#!/bin/bash

ext='vasp'
while getopts ":e:" opt; do
  case $opt in
    e)
      ext="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done
shift "$((OPTIND-1))"

for i in {0..9}; do
    mv *0$i.$ext 0$i*/
done

for i in {10..99}; do
    mv *$i.$ext $i*/
done