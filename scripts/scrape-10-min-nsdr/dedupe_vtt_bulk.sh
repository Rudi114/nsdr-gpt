# Cleans & dedupes all `.vtt` files in nested directories below current directory into txt files
# Requires the `dedupe_vtt.py` script, obviously
find . -type f -name "*.vtt" -exec sh -c 'python3 dedupe_vtt.py "$0" "${0%.vtt}.deduped.txt"' {} \;
