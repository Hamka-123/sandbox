wsl -d GitDeveloper1 -- bash -c "
git config --global user.name 'Andrey Dev' &&
git config --global user.email 'andrey@example.com'
"
# Check
wsl -d GitDeveloper1 -- git config --list