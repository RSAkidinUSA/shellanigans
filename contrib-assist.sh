#!/bin/bash
# Function for getting language of program

# Global variables
program_type=""
program_name=""

# Function for setting up ssh keys for git
setup_ssh () {
	# Add option to automate this
	echo "It's very easy, just head over to https://help.github.com/articles/checking-for-existing-ssh-keys/"
	echo "Followed by https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/"
	echo "Then https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/"
	echo "Finally https://help.github.com/articles/testing-your-ssh-connection/"
}

# Function for getting the type of program. 
# Returns 0 if type chosen, returns 1 if not
get_type () {
	echo "Please enter the type of program you would like to add"
	echo "Existing options are:"
	for existing in $(find . -maxdepth 1 -type d | cut -d / -f 2 | grep -v "\."); do
		echo "-" $existing
	done
	echo "You may also specify an option not listed to create that directory"
	while ( true ); do
		read program_type
		if [ -z $program_type ]; then
			echo "Please enter a program type:"
			continue
		else
			break
		fi
	done
	newProg=true
	for existing in $(find . -maxdepth 1 -type d | cut -d / -f 2 | grep -v "\."); do
		if [ "$existing" == "$program_type" ]; then
			newProg=false
			break
		fi
	done
	if [[ $newProg == true ]]; then
		echo "Make new directory for" $program_type "programs?"
		while ( true ); do
			read resp
			if [ ${resp,,} == "y" ] ||  [ ${resp,,} == "yes" ]; then
				mkdir $program_type
				break
			elif [ ${resp,,} == "n" ] || [ ${resp,,} == "no" ]; then
				return 1
			else
				echo ${resp,,} "is not a valid response. Please select from (yes,y,no,n):"
				continue
			fi
		done
	else
		echo "Make new" $program_type "program?"
		while ( true ); do
			read resp
			if [ ${resp,,} == "y" ] ||  [ ${resp,,} == "yes" ]; then
				break
			elif [ ${resp,,} == "n" ] || [ ${resp,,} == "no" ]; then
				return 1
			else
				echo ${resp,,} "is not a valid response. Please select from (yes,y,no,n):"
				continue
			fi
		done
	fi
	return 0
}

# Function for getting the name of program. 
# Returns 0 if name chosen, returns 1 if not
get_name () {
	echo "Enter the name of the program:"
	while ( true ); do
		read program_name
		if [ -z $program_name ]; then
			echo "Please enter a program name:"
			continue
		else
			break
		fi
	done
}

# Check if user has Github ssh access
ssh -T git@github.com &> .ssh_auth
if [[ $? == 255 ]]; then
	rm .ssh_auth
	echo "You will need to set up ssh keys on Github to use this script"
	setup_ssh
else
	ID=$(cat .ssh_auth | cut -f2 -d" " | cut -f1 -d"!")
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

	# Move to the correct directory
	cd $program_type

	# Get the name of the program
	get_name
	while [ $? -ne 0 ]; do
		get_name
	done

	if [[ $COLLAB == true ]]; then
		# do a branch
		echo $program_type"/"$program_name
	else
		# do a fork
		echo $program_type|rev"/"$program_name|rev
	fi
fi
