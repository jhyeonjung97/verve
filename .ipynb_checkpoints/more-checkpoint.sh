for file in "$@"
do
    if [[ "$file" == *.png ]]; then
        display "$file"
    else
        more "$file"
    fi
done
