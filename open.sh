for file in "$@"
do
    if [[ "$file" == *.png ]]; then
        display "$file"
    else
<<<<<<< HEAD
        more "$file"
    fi
done
=======
        open "$file"
    fi
done
>>>>>>> 43378e7a586f5c8e8c5738b35a1c9094fb2139f0
