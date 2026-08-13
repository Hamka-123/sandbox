#!/bin/bash

: <<README
- Set desired host name - constant
- Check current hostname
- If doesn't match - rename

README

readonly NEW_HOSTNAME="$1"
CURRENT_HOSTNAME="$(hostname)"
readonly CURRENT_HOSTNAME
echo "Current host name $CURRENT_HOSTNAME"

if [[ $CURRENT_HOSTNAME != $NEW_HOSTNAME ]];
then 
	echo "Changing host name.."
	sudo hostnamectl set-hostname "$NEW_HOSTNAME"

else
	echo "Do nothing"

fi