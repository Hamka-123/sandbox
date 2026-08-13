#!/bin/bash

# loop - for

for ((i = 0; i < 5; i++)); do
	echo "i = $i"

done

echo
echo "for i in 22 33 44; do"
for i in 22 33 44; do

	echo "i = $i"

done

echo
echo "for file in ./* ; do"
for file in ./*; do

	echo "file = $file"

	if [[ $file =~ \.sh ]]; then # ← see 'man bash' for valid conditional statements.
		echo "SCRIPT"

	else
		echo "Not SCRIPT"
	fi

done
