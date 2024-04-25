for file in "$@"
do
    if [[ "$file" == *.png ]]; then
        display "$file"
    else
        open "$file"
    fi
done