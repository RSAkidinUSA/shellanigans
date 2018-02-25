#!/bin/bash
# Function for getting language of program
program_type=''

get_type () {
	echo "Please enter the type of program you would like to add"
	echo "Existing options are:"
	for existing in $(find . -maxdepth 1 -type d | cut -d / -f 2 | grep -v '\.'); do
		echo '-' $existing
	done
	read program_type
	newProg=true
	for existing in $(find . -maxdepth 1 -type d | cut -d / -f 2 | grep -v '\.'); do
		if [ "$existing" == "$program_type" ]; then
			newProg=false
			break
		fi
	done
	if [[ $newProg == true ]]; then
		while ( true ); do
			echo "Make new directory for" $program_type "programs?"
			read resp
			if [ ${resp,,} == 'y' ] ||  [ ${resp,,} == 'yes' ]; then
				mkdir $program_type
				break
			elif [ ${resp,,} == 'n' ] || [ ${resp,,} == 'no' ]; then
				return 1
			else
				echo ${resp,,} 'is not a valid response please select from (yes,y,no,n)'
				continue
			fi
		done
	fi
	return 0
}

# Check if user has Github ssh access
ssh -T git@github.com &> .ssh_auth
if [[ $? == 255 ]]; then
	rm .ssh-auth
	echo "You will need to set up ssh keys on Github to use this script"
	# Add option to automate this
	echo "It's very easy, just head over to https://help.github.com/articles/checking-for-existing-ssh-keys/"
	echo "Followed by https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/"
	echo "Then https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/"
	echo "Finally https://help.github.com/articles/testing-your-ssh-connection/"
else
	ID=$(cat .ssh_auth | cut -f2 -d' ' | cut -f1 -d'!')
	COLLAB=false
	rm .ssh_auth
	for i in $(cat .collaborators); do
		if [[ ${ID,,} == ${i,,} ]]; then
			COLLAB=true
			break
		fi
	done
	# Get the the type of program
	get_type
	while [ $? -ne 0 ]; do
		get_type
	done
	# Get the name of the program

	if [[ $COLLAB == true ]]; then
		# do a branch
		echo $program_type
	else
		# do a fork
		echo $program_type|rev
	fi
fi
