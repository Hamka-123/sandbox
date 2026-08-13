#!bin/bash
: <<README
- Set desired hostname - constant
- Check corrent hostname
- If does not match -> rename

README

readonly NEW_HOSTNAME="UbuntuServer6"
CURRENT_HOSTNAME="$(hostname)"
readonly CURRENT_HOSTNAME

echo "Current host name: $CURRENT_HOSTNAME"

if [[ $CURRENT_HOSTNAME != $NEW_HOSTNAME ]]; then
	echo "Changing hostname ..."
	sudo hostnamectl set-hostname "$NEW_HOSTNAME"
else
	echo "Nothing to change"
fi
