#!/bin/bash
rm -f caches.txt
rstor_cli info | grep "Cache Name" | while read line; do
	echo $line | cut -d: -f2 | cut -d' ' -f2>> caches.txt ;
done

