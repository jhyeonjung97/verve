#!/bin/bash

# Get current directory size in kilobytes
size_kb=$(du -sk ./ | awk '{print $1}')
echo "Current directory size: $(du -sh ./ | awk '{print $1}')"

# 1GB = 1024^2 KB
limit=$((1024*1024))

while [ $size_kb -gt $limit ]; do
    echo "Size limit: $((limit/1024))MB"
    
    # Show files that will be deleted
    echo "Files to be deleted:"
    find . -type f -size +${limit}k -exec du -sh {} \; -exec echo "  {}" \;
    
    # Ask for confirmation
    read -p "Do you want to proceed with deletion? (y/n): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        find . -type f -size +${limit}k -exec rm -v {} \;
        size_kb=$(du -sk ./ | awk '{print $1}')
        echo "Size after deletion: $(du -sh ./ | awk '{print $1}')"
    else
        echo "Deletion cancelled."
        break
    fi
    
    limit=$((limit/10))
done

echo "Cleanup completed. Final size: $(du -sh ./ | awk '{print $1}')"



