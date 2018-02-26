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
	# echo "Generating ssh keys for you..."
	# ssh-keygen -t rsa -b 4096 -C $EMAIL -f ~/.ssh/id_rsa_github -N '' -q
	# eval $(ssh-agent -s)
	# ssh-add ~/.ssh/id_rsa_github
	# echo "Please copy and paste the following key into your github ssh keys"
	# echo "(https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/):"
	# echo
	# cat ~/.ssh/id_rsa_github.pub
	# echo

	echo "Then https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/"
	echo "Finally https://help.github.com/articles/testing-your-ssh-connection/"
}

# Function to create a Makefile
manage_make () {
	echo "I don't do anything yet"
}

# Function to create or edit a README.md
manage_readme () {
	ls README.md > /dev/null &> /dev/null
	if [[ $? != 0 ]]; then
		echo "# $1" > README.md
		echo "" >> README.md
	fi
	"${EDITOR:-vi}" README.md
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
		program_type=$(echo $program_type|awk '{gsub(/ /,"-")}1')
		if [ -z $program_type ]; then
			echo "Please enter a program type:"
			continue
		else
			break
		fi
	done
	newProg=true
	for existing in $(find . -maxdepth 1 -type d | cut -d / -f 2 | grep -v "\."); do
		if [ "${existing,,}" == "${program_type,,}" ]; then
			newProg=false
			break
		fi
	done
	if [[ $newProg == true ]]; then
		echo "Make new directory for" $program_type "programs? (y/n)"
		while ( true ); do
			read resp
			if [ ${resp,,} == "y" ] ||  [ ${resp,,} == "yes" ]; then
				mkdir $program_type
				break
			elif [ ${resp,,} == "n" ] || [ ${resp,,} == "no" ]; then
				return 1
			else
				echo ${resp,,} "is not a valid response. Please select from {yes,y,no,n}:"
				continue
			fi
		done
	else
		echo "Make new" $program_type "program? (y/n)"
		while ( true ); do
			read resp
			if [ ${resp,,} == "y" ] ||  [ ${resp,,} == "yes" ]; then
				break
			elif [ ${resp,,} == "n" ] || [ ${resp,,} == "no" ]; then
				return 1
			else
				echo ${resp,,} "is not a valid response. Please select from {yes,y,no,n}:"
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
		program_name=$(echo $program_name|awk '{gsub(/ /,"-")}1')
		if [ -z $program_name ]; then
			echo "Please enter a program name:"
			continue
		else
			break
		fi
	done
	for existing in $(find . -maxdepth 1 -type d | cut -d / -f 2 | grep -v "\."); do
		if [ "${existing,,}" == "${program_name,,}" ]; then
			echo "$existing already exists, please select another name."
			return 1
		fi
	done
	mkdir $program_name
	return 0
}

main () {
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
		manage_readme $program_type

		# Get the name of the program
		get_name
		while [ $? -ne 0 ]; do
			get_name
		done

		# Move to the correct directory
		cd $program_name

		# Edit the readme and makefile
		manage_readme $program_name
		manage_make

		if [[ $COLLAB == true ]]; then
			# do a branch
			git checkout -b $program_name
			git add ../$program_name ../../$program_type
			git commit -m "Initial commit for branch $program_name"
			echo "Push to Github? (y/n)"
			while (true); do
				read resp
				if [ ${resp,,} == "y" ] ||  [ ${resp,,} == "yes" ]; then
					git push --set-upstream origin $program_name && git push
					break
				elif [ ${resp,,} == "n" ] || [ ${resp,,} == "no" ]; then
					break
				else
					echo ${resp,,} "is not a valid response. Please select from {yes,y,no,n}:"
					continue
				fi
			done
			GIT_REPO="https://github.com/RSAkidinUSA/shellanigans"
		else
			# do a fork
			# check if this already a fork...
			git remote rename origin upstream
			git remote set-url upstream 'git@github.com:'RSAkidinUSA'/shellanigans.git'
			git remote add origin 'git@github.com:'$ID'/shellanigans.git'
			GIT_REPO="https://github.com/"$ID"/shellanigans"
		fi

		# Further instructions
		echo "Congratulations! You're ready to go!"
		echo "Make any changes you want, commit them with good messages!"
		echo "Don't forget to push those changes too!"
		echo "When you're ready to get your changes added, head to" $GIT_REPO "and make a pull request!"
		echo "For more help with git, checkout the git_help.md!"
	fi
}

main
