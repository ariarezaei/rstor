#!/bin/bash
rm -f Disks.txt
echo SDA >> Disks.txt
fdisk -l | grep Disk | grep sectors | while read line; do
	s1=$(echo $line | cut -d' ' -f2 | cut -d: -f1)
	s2=$(echo $line | cut -d' ' -f3)
	s3=$(echo $line | cut -d' ' -f4)
	s4="${s1} ${s2} ${s3}";
	echo $s4 >> Disks.txt;
done
