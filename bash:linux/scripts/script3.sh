#!/bin/bash

#create variables
user_name="Bob"

echo "starting script $0 , $1 , User name var is: $user_name"

#Create constant
readonly MY_FOLDER="/etc/"
#MY_FOLDER="" #/home/hamka/scripts/script3.sh: line 11: MY_FOLDER: readonly variable
echo $MY_FOLDER

#Substitutions (vars, commands)
printf "\nCommand:\n"
echo "My host name: $(hostname)"
# Пример:
echo "Today is: $(date +%D)"
echo "Current directory: $(pwd)"
echo "My host name: $(hostname)"

NAME="Admin"
echo "Hello, $NAME"
echo "File_${NAME}_backup.txt"  # Без скобок {} Bash искал бы переменную $NAME_backup

#args array
args_arr=("$@")
echo "${args_arr[1]}"

#heredoc
cat << EOS >> text.txt
sd asd
as dasd
 asd
  asd
   
EOS
# 4. УСЛОВИЯ (Числа)
# -eq (равно), -ne (не равно), -lt (<), -le (<=), -gt (>), -ge (>=)
if [[ 1 -gt 10 ]]; then
    echo "Число больше 10"
elif [[ 1 -eq 10 ]]; then
    echo "Число равно 10"
elif [[ 1 -lt 10 ]]; then
    echo "Число меньше 10"    
else
    echo "Число меньше 10"
fi

CURRENT_USER="$(whoami)"
echo "$CURRENT_USER"

ACCEPTED_USER="user2"

if [[ $CURRENT_USER == $ACCEPTED_USER ]]
then
    echo "Accepted"
else
    echo "Denied"
fi

for file in /home/hamka/scripts/*; do
    echo "file = $file"

    if [[ $file =~ \.sh ]]
    then
        echo "SCRIPT"
    else
        echo "NOT SCRIPT"
    fi

done

#INTERFACES=(lo ens38 LAN WAN) #Array
#INTERFACES=($(ip -o link show | awk -F': ' '{print $2}'))
# Используем readarray, чтобы сохранить целые строки, а не отдельные слова
readarray -t INTERFACES < <(ip -o link show | awk '{
    # Ищем имя интерфейса: это второе поле, убираем двоеточие в конце
    iface = $2; sub(/:$/, "", iface);
    
    # Ищем поле, которое идет СРАЗУ ПОСЛЕ "link/ether"
    for (i=1; i<=NF; i++) {
        if ($i == "link/ether") {
            mac = $(i+1);
            print iface ": " mac;
            next;
        }
    }
}')

# Вывод результата
for i in "${INTERFACES[@]}"; do
    echo "Найдено: $i"
done
