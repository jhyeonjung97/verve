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

# Move files with single-digit or leading-zero numbers
for i in {0..9}; do
    dir=$(echo $i*/)
    files=(*$i.$ext)
    if [[ -d $dir ]] && [[ ${#files[@]} -gt 0 ]]; then
        mv *$i.$ext $dir
    fi
done

# # Move files with single-digit or leading-zero numbers
# for i in {0..9}; do
#     dir=$(echo 0$i*/)
#     files=(*0$i.$ext)
#     if [[ -d $dir ]] && [[ ${#files[@]} -gt 0 ]]; then
#         mv *0$i.$ext $dir
#     fi
# done

# # Move files with two-digit numbers from 10 to 99
# for i in {10..99}; do
#     dir=$(echo $i*/)
#     files=(*$i.$ext)
#     if [[ -d $dir ]] && [[ ${#files[@]} -gt 0 ]]; then
#         mv *$i.$ext $dir
#     fi
# done
