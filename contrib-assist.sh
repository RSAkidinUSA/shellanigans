#!/bin/bash
# Check if user has Github ssh access
ssh -T git@github.com &> .ssh-auth
if [[ $? == 255 ]]; then
	rm .ssh-auth
	echo "You will need to set up ssh keys on Github to use this script"
	# Add option to automate this
	echo "It's very easy, just head over to https://help.github.com/articles/checking-for-existing-ssh-keys/"
	echo "Followed by https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/"
	echo "Then https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/"
	echo "Finally https://help.github.com/articles/testing-your-ssh-connection/"
else
	ID=$(cat .ssh-auth | cut -f2 -d' ' | cut -f1 -d'!')
	COLLAB=false
	rm .ssh-auth
	for i in $(cat .collaborators); do
		if [[ ${ID,,} == ${i,,} ]]; then
			COLLAB=true
			break
		fi
	done
	if [[ $COLLAB == true ]]; then
		# do a branch
		echo $ID
	else
		# do a fork
		echo $ID|rev
	fi
fi

# Get github password
# Authenticate to github