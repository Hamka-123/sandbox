#!/bin/bash 
printf "\nIP ADDRESS\n"
ip address
printf "\nIP LINK\n"
ip link

#redirect output (rewrite):
#ip link > ip_link.txt
#redirect output (append):
#ip link >> ip_link.txt

#redirect input
#bash < "command.sh" #| > ttt.txt ???


