# Add remote (SSH + port 2222)
wsl -d GitDeveloper1 -- bash -c "
cd ~/project1 &&
git remote add origin ssh://git@172.26.74.84:2222/srv/git/project1.git
"