#!/bin/bash

[ -z "$1" ] && echo "Usage: $0 <file.html>" && exit 1

cat $1 | grep ssr: | cut -d'"' -f 8 | grep -v ^$ || exit 1

exit 0

