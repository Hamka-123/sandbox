#!/bin/bash

## VARIABLES / CONSTANTS
# Create variable:
user_name="Bob"

echo "Starting script $0  User name variable value: $user_name" 

# Create constant
readonly MY_FOLDER="/etc/"
#MY_FOLDER="" # ERROR: script2_bash_variables.sh: line 10: MY_FOLDER: readonly variable

# Substitutions (vars, commands)
printf "\nCommands substitution:\n"
echo "My host name = $(hostname)" # My host name = ubuntu-server-6

# Special variables:
: <<'REM'
$0 - cirrent script name
&1, $2, ...  script arguments
$# - number ow args
$@ - all arguments, separated
$* - all arguments string
$? - scripr exit status

REM

echo "Arguments"
echo "$@"

# args array:
args_array=("$@")
echo "${args_array[1]}"

# heredoc

cat <<EOS > ttt.txt
uiyg yiug 
iouoiu 
oiug ioug
iu oiu
User name: $user_name
EOS