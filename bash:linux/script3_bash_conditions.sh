#!/bin/bash

# if

# if [ 2 -gt 0 ]; then
if [ 2 -lt 0 ]; then
echo "True"

else
echo "False"

fi # End if
# numbers comparison keys: -lt -gt -le -ge -ne -eq

CURRENT_USER="$(whoami)"
echo "$CURRENT_USER"

ACCEPRED_USER="user1"

# String comparison: !=   ==

if [[ $CURRENT_USER == $ACCEPRED_USER ]]
then
   echo "Accepted"    
else
   echo "Denied" 
fi
