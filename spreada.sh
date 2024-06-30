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

mv *00.$ext 00*/
mv *01.$ext 01*/
mv *02.$ext 02*/
mv *03.$ext 03*/
mv *04.$ext 04*/
mv *05.$ext 05*/
mv *06.$ext 06*/
mv *07.$ext 07*/
mv *08.$ext 08*/
mv *09.$ext 09*/
mv *10.$ext 10*/
mv *11.$ext 11*/
mv *12.$ext 12*/